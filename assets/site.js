/* ============================================================
   nggkhaiz.js.org — behaviour
   No dependencies. Everything degrades to plain HTML.
   ============================================================ */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- copy ---------------- */

  var copy = {
    vi: {
      title: "Nguyễn Gia Khải — 14, builder",
      "a11y.skip": "Bỏ qua tới nội dung",
      "nav.about": "Giới thiệu",
      "nav.work": "Dự án",
      "nav.domains": "Lĩnh vực",
      "nav.contact": "Liên hệ",
      "hero.kicker": "Xin chào",
      "hero.age": "14 tuổi",
      "hero.role": "Học sinh · Người viết code",
      "hero.tagline":
        "Mình viết code, phá thử, rồi ghép lại — để một ý tưởng thành thứ người khác chạy được thật.",
      "hero.ctaContact": "Liên hệ",
      "hero.ctaCredentials": "Xem năng lực",
      "hero.scroll": "Cuộn",
      "facts.fieldKey": "Lĩnh vực",
      "facts.fieldValue": "Code & thiết kế",
      "facts.locationKey": "Nơi ở",
      "facts.locationValue": "Bắc Giang, Việt Nam",
      "facts.siteKey": "Trang",
      "facts.statusKey": "Trạng thái",
      "facts.statusValue": "Học và làm công khai",
      "about.kicker": "Giới thiệu",
      "about.title": "Chỗ giao nhau giữa tò mò và tay nghề.",
      "about.lede": "Mình không cố tỏ ra chuyên nghiệp. Mình cố giỏi hơn, công khai, từng dòng một.",
      "about.p1":
        "Mình là <strong>Khải</strong>, 14 tuổi, ở Bắc Giang. Mình bắt đầu với C++ vì trình biên dịch rất thẳng thắn: hoặc chạy, hoặc không. Thói quen đó ở lại — mình thích chương trình nhỏ, dự án thật, và code có thể giải thích từng dòng.",
      "about.p2":
        "Phần lớn thứ mình làm nằm công khai: một trình quét code bị làm rối bằng Python, một panel chạy được bằng Docker, và trang này — HTML/CSS viết tay, không framework, không bước build. Mình thích cảm giác đẩy lên rồi xem nó có sống không.",
      "about.locationKey": "Vị trí",
      "about.locationValue": "Bắc Giang, Việt Nam",
      "about.focusKey": "Đang tập trung",
      "about.focusValue": "C++, Python, web thuần",
      "about.learnKey": "Đang học",
      "about.learnValue": "Hệ thống, bảo mật cơ bản",
      "cred.kicker": "Năng lực",
      "cred.title": "Con số nhỏ, nhưng là thật.",
      "cred.lede": "Không có chứng chỉ để khoe. Chỉ có repo, commit và những thứ đã chạy được.",
      "cred.one.title": "Repo công khai",
      "cred.one.text":
        "Từ tháng 12/2025, mỗi repo là một lý do để học thêm: công cụ, thử nghiệm, panel nhỏ.",
      "cred.two.title": "Ngôn ngữ trong repo",
      "cred.two.text":
        "C++, Python, TypeScript, JavaScript, HTML/CSS, Rust — chọn theo việc cần làm, không theo mốt.",
      "cred.three.title": "Điều đang theo đuổi",
      "cred.three.text":
        "Hiểu máy chạy thế nào, viết code đọc được, và giữ thói quen đẩy sản phẩm ra ngoài.",
      "work.kicker": "Dự án",
      "work.title": "Vài thứ đã làm xong.",
      "work.lede": "Chọn lọc, không phải tất cả. Cái nào cũng có link để bạn tự kiểm tra.",
      "work.one.text":
        "Trình quét code bị làm rối và một kệ file công khai. Mình muốn biết code rối giấu gì, nên viết luôn công cụ đi tìm.",
      "work.two.text":
        "Panel tự host, đóng gói Docker, chạy được từ một Procfile. Làm để xem một bảng điều khiển nhỏ có thể đi xa tới đâu.",
      "work.three.text":
        "Chính trang bạn đang đọc: HTML và CSS viết tay, không framework, không bundler, deploy bằng GitHub Pages.",
      "work.four.title": "Profile này",
      "work.four.text":
        "README và toàn bộ ảnh SVG của profile, sinh ra từ một script Python nhỏ để sáng/tối luôn khớp nhau.",
      "domains.kicker": "Lĩnh vực",
      "domains.title": "Những gì mình chạm tới.",
      "domains.lede": "Không phải bảng kỹ năng đầy đủ — chỉ là những thứ đã dùng cho một dự án thật.",
      "domains.note":
        "Thứ mình đang đọc thêm: cách CPU và bộ nhớ làm việc, cách một request đi qua một hệ thống, và cách viết giao diện ít nhưng đúng.",
      "contact.kicker": "Liên hệ",
      "contact.title": "Một đường thẳng.",
      "contact.cta": "Nhắn mình trên GitHub",
      "contact.where": "Nơi khác",
      "contact.repo": "Repo của profile này",
      "contact.site": "Trang",
      "contact.top": "Về đầu trang",
      "footer.rights": "làm bằng tay",
      "footer.top": "Lên đầu trang"
    },

    en: {
      title: "Nguyễn Gia Khải — 14, builder",
      "a11y.skip": "Skip to content",
      "nav.about": "About",
      "nav.work": "Work",
      "nav.domains": "Domains",
      "nav.contact": "Contact",
      "hero.kicker": "Welcome",
      "hero.age": "14 years old",
      "hero.role": "Student · Code writer",
      "hero.tagline":
        "I write code, break it on purpose, and put it back together — so an idea becomes something you can actually run.",
      "hero.ctaContact": "Get in touch",
      "hero.ctaCredentials": "View credentials",
      "hero.scroll": "Scroll",
      "facts.fieldKey": "Field",
      "facts.fieldValue": "Code & design",
      "facts.locationKey": "Based in",
      "facts.locationValue": "Bắc Giang, Việt Nam",
      "facts.siteKey": "Site",
      "facts.statusKey": "Status",
      "facts.statusValue": "Learning in public",
      "about.kicker": "About",
      "about.title": "Where curiosity meets craft.",
      "about.lede": "I am not trying to look senior. I am trying to get better, in public, one line at a time.",
      "about.p1":
        "I am <strong>Khải</strong>, 14, from Bắc Giang. I started with C++ because a compiler is brutally honest: it runs or it does not. The habit stuck — I like small programs, real projects and code I can explain line by line.",
      "about.p2":
        "Most of what I build lives in public: a Python scanner for obfuscated code, a Docker-ready panel, and this site — hand-written HTML and CSS, no framework, no build step. I like pushing something live and finding out whether it survives.",
      "about.locationKey": "Location",
      "about.locationValue": "Bắc Giang, Việt Nam",
      "about.focusKey": "Focus",
      "about.focusValue": "C++, Python, plain web",
      "about.learnKey": "Learning",
      "about.learnValue": "Systems, security basics",
      "cred.kicker": "Credentials",
      "cred.title": "Small numbers, all of them real.",
      "cred.lede": "No certificates to show off. Just repos, commits and things that already ran.",
      "cred.one.title": "Public repositories",
      "cred.one.text":
        "Since December 2025 every repo has been a reason to learn something: tools, experiments, small panels.",
      "cred.two.title": "Languages in my repos",
      "cred.two.text":
        "C++, Python, TypeScript, JavaScript, HTML/CSS, Rust — picked per job, not per trend.",
      "cred.three.title": "What I am after",
      "cred.three.text":
        "Understanding how the machine actually works, writing readable code, and keeping the habit of shipping.",
      "work.kicker": "Work",
      "work.title": "A few things, finished.",
      "work.lede": "Selected, not everything. Each one links somewhere you can check.",
      "work.one.text":
        "An obfuscation scanner and a public file shelf. I wanted to know what obfuscated code hides, so I wrote the tool that looks for it.",
      "work.two.text":
        "A self-hosted panel with Docker packaging, deployable from a Procfile. Built to see how far one small control panel can go.",
      "work.three.text":
        "The page you are reading: hand-written HTML and CSS, no framework, no bundler, deployed on GitHub Pages.",
      "work.four.title": "This profile",
      "work.four.text":
        "The README and every SVG asset behind it, generated by a small Python script so dark and light stay in sync.",
      "domains.kicker": "Domains",
      "domains.title": "What I actually touch.",
      "domains.lede": "Not a full skill matrix — only the things that carried a real project.",
      "domains.note":
        "Currently reading up on: how CPU and memory work, how a request travels through a system, and how to write interfaces that say less but mean more.",
      "contact.kicker": "Contact",
      "contact.title": "A direct line.",
      "contact.cta": "Message me on GitHub",
      "contact.where": "Elsewhere",
      "contact.repo": "This profile's repo",
      "contact.site": "Pages",
      "contact.top": "Back to top",
      "footer.rights": "made by hand",
      "footer.top": "Back to top"
    }
  };

  /* ---------------- language ---------------- */

  var langBtn = document.getElementById("lang-toggle");
  var langCurrent = document.getElementById("lang-current");
  var hasCopy = document.querySelector("[data-i18n], [data-i18n-html]") !== null;

  function applyLang(lang) {
    var dict = copy[lang] || copy.vi;
    root.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var value = dict[el.getAttribute("data-i18n")];
      if (value) el.textContent = value;
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var value = dict[el.getAttribute("data-i18n-html")];
      if (value) el.innerHTML = value;
    });

    if (dict.title) document.title = dict.title;
    if (langCurrent) langCurrent.textContent = lang.toUpperCase();

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
    if (themeColor) themeColor.setAttribute("content", dark ? "#0a0a0b" : "#f6f4f0");
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

  /* ---------------- misc ---------------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
