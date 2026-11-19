/* ============================================================
   nggkhaiz.js.org — behaviour
   No dependencies. Everything degrades to plain HTML.
   ============================================================ */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;


  /* ---------------- copy ---------------- */

  var copy = window.NK_COPY || { vi: {}, en: {} };

  /* ---------------- language ---------------- */

  var langBtn = document.getElementById("lang-toggle");
  var langCurrent = document.getElementById("lang-current");
  var langOther = document.getElementById("lang-other");
  var hasCopy =
    document.documentElement.hasAttribute("data-lang-switch") && typeof window.NK_COPY === "object";

  function dictFor(lang) {
    if (copy[lang]) return copy[lang];
    return copy.vi || {};
  }

  function applyLang(lang) {
    var dict = dictFor(lang);
    root.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var value = dict[el.getAttribute("data-i18n")];
      if (value) el.textContent = value;
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var value = dict[el.getAttribute("data-i18n-html")];
      if (value) el.innerHTML = value;
    });

    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var value = dict[el.getAttribute("data-i18n-aria")];
      if (value) el.setAttribute("aria-label", value);
    });

    if (langCurrent) langCurrent.textContent = lang.toUpperCase();
    if (langOther) langOther.textContent = "/" + (lang === "vi" ? "EN" : "VI");

    try {
      localStorage.setItem("nk-lang", lang);
    } catch (err) {
      /* storage can be unavailable; the page still renders */
    }
  }

  var storedLang = null;
  try {
    storedLang = localStorage.getItem("nk-lang");
  } catch (err) {
    storedLang = null;
  }

  var initialLang =
    storedLang || ((navigator.language || "vi").toLowerCase().indexOf("vi") === 0 ? "vi" : "en");

  if (hasCopy) {
    applyLang(initialLang);
  }

  if (langBtn && hasCopy) {
    langBtn.addEventListener("click", function () {
      applyLang(root.lang === "vi" ? "en" : "vi");
    });
  }

  /* ---------------- theme ---------------- */

  var themeBtn = document.getElementById("theme-toggle");
  var sun = document.getElementById("icon-sun");
  var moon = document.getElementById("icon-moon");
  var themeColor = document.querySelector('meta[name="theme-color"]');

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var dark = theme === "dark";
    if (sun) sun.hidden = !dark;
    if (moon) moon.hidden = dark;
    if (themeColor) themeColor.setAttribute("content", dark ? "#1e1e2e" : "#eff1f5");
    try {
      localStorage.setItem("nk-theme", theme);
    } catch (err) {
      /* ignore */
    }
  }

  var storedTheme = null;
  try {
    storedTheme = localStorage.getItem("nk-theme");
  } catch (err) {
    storedTheme = null;
  }

  applyTheme(
    storedTheme ||
      (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark")
  );

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  /* ---------------- header, progress, active nav ---------------- */

  var header = document.getElementById("header");
  var progress = document.getElementById("progress");
  var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a"));

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);

    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var ratio = max > 0 ? Math.min(1, y / max) : 0;
      progress.style.transform = "scaleX(" + ratio + ")";
    }

    var activeId = null;
    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top <= window.innerHeight * 0.42) {
        activeId = section.id;
      }
    });

    navLinks.forEach(function (link) {
      link.classList.toggle("is-active", link.getAttribute("href") === "#" + activeId);
    });
  }

  var ticking = false;
  window.addEventListener(
    "scroll",
    function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        onScroll();
        ticking = false;
      });
    },
    { passive: true }
  );
  onScroll();

  /* ---------------- reveal on scroll ---------------- */

  var revealItems = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach(function (el) {
      el.classList.add("is-in");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.12 }
    );

    revealItems.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------------- copy contact handles ---------------- */

  Array.prototype.forEach.call(document.querySelectorAll("[data-copy]"), function (btn) {
    var hint = btn.querySelector(".contact__copy-hint");

    function label(dictKey, fallback) {
      return dictFor(root.lang)[dictKey] || fallback;
    }

    function done() {
      btn.classList.add("is-copied");
      if (hint) hint.textContent = label("contact.copied", "copied");
      window.setTimeout(function () {
        btn.classList.remove("is-copied");
        if (hint) hint.textContent = label("contact.copy", "copy");
      }, 1800);
    }

    function legacyCopy(text) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy");
        done();
      } catch (err) {
        /* clipboard unavailable: the handle is visible on the page anyway */
      }
      document.body.removeChild(area);
    }

    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy") || "";
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {
          legacyCopy(text);
        });
      } else {
        legacyCopy(text);
      }
    });
  });

  /* ---------------- misc ---------------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
