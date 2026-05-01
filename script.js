const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav a");
const yearTarget = document.querySelector("#year");
const revealItems = document.querySelectorAll(".reveal");
const mobileCollapsibles = document.querySelectorAll("[data-mobile-collapsible]");

if (yearTarget) {
  yearTarget.textContent = new Date().getFullYear();
}

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.dataset.open === "true";
    siteNav.dataset.open = String(!isOpen);
    navToggle.setAttribute("aria-expanded", String(!isOpen));
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      siteNav.dataset.open = "false";
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

if (mobileCollapsibles.length) {
  const mobileQuery = window.matchMedia("(max-width: 760px)");
  const syncMobileCollapsibles = () => {
    mobileCollapsibles.forEach((item) => {
      item.open = !mobileQuery.matches || item.hasAttribute("data-mobile-open");
    });
  };

  syncMobileCollapsibles();

  if (typeof mobileQuery.addEventListener === "function") {
    mobileQuery.addEventListener("change", syncMobileCollapsibles);
  } else {
    mobileQuery.addListener(syncMobileCollapsibles);
  }
}

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.18,
    },
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}
