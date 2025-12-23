(function () {
  const KEY = "site_lang";
  const supported = new Set(["ua", "en"]);

  function setTitle(lang) {
    const map = {
      "index.html": {
        ua: "Про мене — Дмитро",
        en: "About — Dmytro",
      },
      "projects.html": {
        ua: "Проєкти — Дмитро",
        en: "Projects — Dmytro",
      },
      "gdd.html": {
        ua: "GDD — Carnage Club",
        en: "GDD — Carnage Club",
      }
    };

    const page = location.pathname.split("/").pop();
    if (map[page]) {
      document.title = map[page][lang];
    }
  }

  function applyLang(lang) {
    if (!supported.has(lang)) lang = "ua";

    document.documentElement.lang = lang === "ua" ? "uk" : "en";

    document.querySelectorAll("[data-i18n]").forEach(el => {
      el.hidden = el.dataset.i18n !== lang;
    });

    document.querySelectorAll(".lang-btn[data-lang]").forEach(btn => {
      const active = btn.dataset.lang === lang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });

    setTitle(lang);
    localStorage.setItem(KEY, lang);
  }

  function init() {
    const urlLang = new URLSearchParams(location.search).get("lang");
    const saved = localStorage.getItem(KEY);
    const browser = (navigator.language || "uk").toLowerCase().startsWith("uk") ? "ua" : "en";

    const lang = supported.has(urlLang)
      ? urlLang
      : supported.has(saved)
        ? saved
        : browser;

    applyLang(lang);

    document.querySelectorAll(".lang-btn[data-lang]").forEach(btn => {
      btn.addEventListener("click", () => applyLang(btn.dataset.lang));
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();