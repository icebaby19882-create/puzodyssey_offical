#!/usr/bin/env python3
"""Validate PuzOdyssey B2B GEO static-site requirements."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://puzodyssey.com"

GEO_PAGES = [
    "wholesale-puzzle-boards.html",
    "puzzle-board-distributor.html",
    "rotating-tilting-puzzle-board.html",
    "puzzle-board-sizes.html",
]

REQUIRED_TERMS = [
    "PuzOdyssey",
    "wholesale",
    "retailers",
    "distributors",
    "United States",
    "Canada",
    "Europe",
    "partnerships@puzodyssey.com",
]

FORBIDDEN_PLACEHOLDERS = [
    "+1 (add number)",
    "add WeChat ID",
    "TBD",
    "TODO",
]


class SiteHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_count = 0
        self.canonical = ""
        self.links: set[str] = set()
        self.json_ld: list[str] = []
        self._in_script = False
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and attrs_dict.get("href"):
            self.links.add(attrs_dict["href"] or "")
        if tag == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href") or ""
        if tag == "script" and attrs_dict.get("type") == "application/ld+json":
            self._in_script = True
            self._script_chunks = []

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_script:
            self.json_ld.append("".join(self._script_chunks).strip())
            self._in_script = False
            self._script_chunks = []


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.exists():
        raise AssertionError(f"Missing required file: {path}")
    return file_path.read_text(encoding="utf-8")


def parse_html(path: str) -> tuple[str, SiteHTMLParser]:
    html = read(path)
    parser = SiteHTMLParser()
    parser.feed(html)
    return html, parser


def json_ld_types(parser: SiteHTMLParser, path: str) -> set[str]:
    types: set[str] = set()
    for block in parser.json_ld:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path} has invalid JSON-LD: {exc}") from exc

        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_type = node.get("@type")
            if isinstance(node_type, list):
                types.update(str(item) for item in node_type)
            elif node_type:
                types.add(str(node_type))
    return types


def assert_terms(text: str, terms: list[str], context: str) -> None:
    missing = [term for term in terms if term not in text]
    if missing:
        raise AssertionError(f"{context} missing terms: {', '.join(missing)}")


def assert_no_placeholders(text: str, context: str) -> None:
    found = [term for term in FORBIDDEN_PLACEHOLDERS if term in text]
    if found:
        raise AssertionError(f"{context} contains placeholders: {', '.join(found)}")


def test_llms_txt() -> None:
    text = read("llms.txt")
    assert text.startswith("# PuzOdyssey\n"), "llms.txt must start with a single H1"
    assert f"{SITE}/" in text, "llms.txt must include canonical site URL"
    assert_terms(text, REQUIRED_TERMS, "llms.txt")
    assert "What We Do Not Claim" in text, "llms.txt must avoid unconfirmed B2B claims"
    assert_no_placeholders(text, "llms.txt")


def test_robots_txt() -> None:
    text = read("robots.txt")
    assert "User-agent: OAI-SearchBot" in text, "robots.txt should explicitly allow OAI-SearchBot"
    assert "User-agent: ChatGPT-User" in text, "robots.txt should explicitly allow ChatGPT-User"
    assert f"Sitemap: {SITE}/sitemap.xml" in text, "robots.txt must point to sitemap"


def test_homepage_links_and_schema() -> None:
    html, parser = parse_html("index.html")
    assert_terms(html, ["North America", "Europe", "wholesale", "distributors"], "index.html")
    assert_no_placeholders(html, "index.html")
    for page in GEO_PAGES:
        assert f"./{page}" in parser.links, f"Homepage must link to {page}"

    types = json_ld_types(parser, "index.html")
    for expected_type in ["Organization", "WebSite", "WebPage", "Product", "FAQPage"]:
        assert expected_type in types, f"index.html missing {expected_type} JSON-LD"


def test_geo_pages() -> None:
    for page in GEO_PAGES:
        html, parser = parse_html(page)
        assert parser.h1_count == 1, f"{page} must have exactly one H1"
        assert parser.canonical == f"{SITE}/{page}", f"{page} has wrong canonical URL"
        assert "mailto:partnerships@puzodyssey.com" in html, f"{page} missing email CTA"
        assert_terms(html, REQUIRED_TERMS, page)
        assert_no_placeholders(html, page)

        types = json_ld_types(parser, page)
        assert "WebPage" in types, f"{page} missing WebPage JSON-LD"
        assert "FAQPage" in types, f"{page} missing FAQPage JSON-LD"


def test_sitemap() -> None:
    text = read("sitemap.xml")
    root = ET.fromstring(text)
    urls = {
        loc.text or ""
        for loc in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    }
    expected_urls = {f"{SITE}/", *(f"{SITE}/{page}" for page in GEO_PAGES)}
    missing = sorted(expected_urls - urls)
    if missing:
        raise AssertionError(f"sitemap.xml missing URLs: {', '.join(missing)}")

    lastmods = re.findall(r"<lastmod>([^<]+)</lastmod>", text)
    assert lastmods, "sitemap.xml must include lastmod values"
    for value in lastmods:
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), f"Invalid lastmod format: {value}"


def test_headers() -> None:
    text = read("_headers")
    assert "/llms.txt" in text, "_headers must define llms.txt content type"
    assert "Content-Type: text/plain; charset=utf-8" in text, "llms.txt must be served as UTF-8 text"


def main() -> int:
    tests = [
        test_llms_txt,
        test_robots_txt,
        test_homepage_links_and_schema,
        test_geo_pages,
        test_sitemap,
        test_headers,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 - validation script reports all failures.
            failures.append(f"FAIL {test.__name__}: {exc}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("All GEO checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
