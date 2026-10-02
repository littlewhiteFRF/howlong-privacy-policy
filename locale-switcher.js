(() => {
  const picker = document.querySelector("#locale-picker");
  if (!picker) return;

  const sections = [...document.querySelectorAll("[data-locale-section]")];
  const locales = new Set([...picker.options].map((option) => option.value));
  const isSupported = (tag) => locales.has(tag);

  function resolveLocale(tag) {
    const normalized = tag.replaceAll("_", "-");
    if (isSupported(normalized)) return normalized;
    const lower = normalized.toLowerCase();
    const exact = [...locales].find((locale) => locale.toLowerCase() === lower);
    if (exact) return exact;
    if (lower.startsWith("zh")) {
      return /hant|tw|hk|mo/.test(lower) ? "zh-Hant" : "zh-Hans";
    }
    if (lower.startsWith("en")) return /-gb|uk/.test(lower) ? "en-GB" : "en-US";
    if (lower.startsWith("es")) return "es-ES";
    if (lower.startsWith("pt")) return "pt-BR";
    const base = lower.split("-")[0];
    const match = [...locales].find((locale) => locale.toLowerCase() === base);
    return match || "en-US";
  }

  function setLocale(locale, updateAddress) {
    const section = sections.find((item) => item.dataset.localeSection.split(/\s+/).includes(locale));
    if (!section) return;

    picker.value = locale;
    sections.forEach((item) => { item.hidden = item !== section; });
    document.querySelectorAll("[data-default-content]").forEach((item) => {
      item.hidden = !["zh-Hans", "en-US", "en-GB"].includes(locale);
    });
    document.documentElement.lang = locale;
    document.documentElement.dir = ["ar", "ur"].includes(locale) ? "rtl" : "ltr";
    section.lang = locale;

    if (section.dataset.pageTitle) {
      document.title = `${section.dataset.pageTitle} — HowLong`;
      const heading = document.querySelector("#page-title");
      if (heading) heading.textContent = section.dataset.pageTitle;
      const summary = document.querySelector("#page-summary");
      if (summary) summary.textContent = section.dataset.summary || "";
      const updated = document.querySelector("#page-updated");
      if (updated) updated.textContent = section.dataset.updated || "2026-09-26";
      const description = document.querySelector('meta[name="description"]');
      if (description) description.content = section.dataset.summary || section.dataset.pageTitle;
    }

    document.querySelectorAll("[data-language-link]").forEach((link) => {
      const destination = new URL(link.dataset.languageLink, window.location.href);
      destination.searchParams.set("lang", locale);
      link.href = destination.href;
    });

    if (updateAddress) {
      const address = new URL(window.location.href);
      address.searchParams.set("lang", locale);
      window.history.replaceState(null, "", address);
    }
  }

  const requested = new URLSearchParams(window.location.search).get("lang");
  const initial = requested && isSupported(requested)
    ? requested
    : resolveLocale(navigator.languages?.[0] || navigator.language || "en-US");

  picker.addEventListener("change", () => setLocale(picker.value, true));
  setLocale(initial, false);
})();
