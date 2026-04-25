# PuzOdyssey B2B GEO Design

## Goal

Improve PuzOdyssey's visibility and accuracy in generative search answers for B2B wholesale and distribution queries, especially from buyers in the United States, Canada, and Europe.

## Audience

The primary audience is retail buyers, online sellers, regional distributors, and category managers looking for premium wooden puzzle boards. The site should help AI systems and human buyers understand that PuzOdyssey is a wholesale-friendly puzzle board brand with a focused product collection.

## Constraints

- Keep the current homepage layout mostly unchanged.
- Do not claim local warehouses, certifications, fixed MOQ, fixed pricing, delivery timelines, or exclusive territory rights unless those facts are confirmed later.
- Keep all new content visible and useful to real buyers; no hidden SEO-only pages.
- Use clear English copy for North America and Europe before considering localized pages.

## Information Architecture

The homepage remains the brand entry point. Four supporting B2B pages provide focused, AI-readable content:

- `/wholesale-puzzle-boards.html`: wholesale puzzle boards for retailers and online sellers.
- `/puzzle-board-distributor.html`: distribution and regional partnership positioning.
- `/rotating-tilting-puzzle-board.html`: product feature explanation.
- `/puzzle-board-sizes.html`: 1,000, 1,500, and 2,000-piece puzzle board sizes.

Each page includes a single H1, short intro, buyer-focused sections, FAQ, and a mailto CTA for `partnerships@puzodyssey.com`.

## Machine-Readable Layer

- Add `/llms.txt` as a concise AI-readable business identity file.
- Update `robots.txt` to explicitly allow OAI-SearchBot and ChatGPT-User while retaining general crawl access.
- Update `sitemap.xml` with all new pages and accurate `lastmod` dates.
- Add JSON-LD to the homepage and new pages using relevant schema types: `Organization`, `WebSite`, `WebPage`, `ItemList`, and `FAQPage`.
- Avoid `Product` JSON-LD until public pricing, offers, reviews, or aggregate ratings are available, because Google product rich results require those fields.

## Homepage Changes

The homepage should receive only lightweight visible changes:

- Add North America and Europe language in the wholesale section.
- Add natural links from the wholesale section to the four B2B pages.
- Replace placeholder partner contact text with non-committal text that does not imply unavailable contact channels.
- Add a homepage Product JSON-LD block aligned with visible product information.

## Verification

Create and maintain a local static validation script that checks:

- Required GEO files exist.
- Homepage links to all GEO pages.
- Each GEO page has one H1, canonical URL, mailto CTA, required B2B terms, and valid JSON-LD.
- `llms.txt`, `robots.txt`, and `sitemap.xml` include the expected signals.
- Placeholder text is not present.
