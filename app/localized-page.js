(() => {
  const picker = document.querySelector("#locale-picker");
  if (!picker) return;

  const copyURL = new URL("locales.json", document.currentScript.src);

  fetch(copyURL)
    .then((response) => {
      if (!response.ok) throw new Error(`Locale copy request failed: ${response.status}`);
      return response.json();
    })
    .then((locales) => {
      const localeTags = Object.keys(locales);
      localeTags.forEach((tag) => {
        const option = document.createElement("option");
        option.value = tag;
        option.textContent = locales[tag].localeName;
        picker.append(option);
      });

      const isSupported = (tag) => Object.hasOwn(locales, tag);
      const resolveLocale = (tag) => {
        const normalized = tag.replaceAll("_", "-");
        if (isSupported(normalized)) return normalized;
        const lower = normalized.toLowerCase();
        const exact = localeTags.find((locale) => locale.toLowerCase() === lower);
        if (exact) return exact;
        if (lower.startsWith("zh")) return /hant|tw|hk|mo/.test(lower) ? "zh-Hant" : "zh-Hans";
        if (lower.startsWith("en")) return /-gb|uk/.test(lower) ? "en-GB" : "en-US";
        if (lower.startsWith("es")) return "es-ES";
        if (lower.startsWith("pt")) return "pt-BR";
        return localeTags.find((locale) => locale.toLowerCase() === lower.split("-")[0]) || "en-US";
      };

      const localizedURL = (locale) => {
        const url = new URL(window.location.href);
        url.searchParams.set("lang", locale);
        return url;
      };

      const setLocale = (locale, updateAddress) => {
        const content = locales[locale] || locales["en-US"];
        picker.value = locale;
        document.documentElement.lang = locale;
        document.documentElement.dir = ["ar", "ur"].includes(locale) ? "rtl" : "ltr";

        document.querySelectorAll("[data-i18n]").forEach((element) => {
          const value = content[element.dataset.i18n];
          if (typeof value === "string") element.textContent = value;
        });
        if (typeof content.languageLabel === "string") picker.setAttribute("aria-label", content.languageLabel);

        document.querySelectorAll("[data-i18n-attr]").forEach((element) => {
          element.dataset.i18nAttr.split(",").forEach((pair) => {
            const [attribute, key] = pair.trim().split(":");
            if (attribute && typeof content[key] === "string") element.setAttribute(attribute, content[key]);
          });
        });

        document.title = content.title;
        const description = document.querySelector('meta[name="description"]');
        const ogTitle = document.querySelector('meta[property="og:title"]');
        const ogDescription = document.querySelector('meta[property="og:description"]');
        if (description) description.content = content.description;
        if (ogTitle) ogTitle.content = content.title;
        if (ogDescription) ogDescription.content = content.description;

        document.querySelectorAll("a[data-language-link]").forEach((link) => {
          const target = new URL(link.dataset.languageLink, window.location.href);
          target.searchParams.set("lang", locale);
          link.href = target.href;
        });

        document.querySelectorAll('link[rel="alternate"][hreflang]').forEach((link) => link.remove());
        localeTags.forEach((tag) => {
          const alternate = document.createElement("link");
          alternate.rel = "alternate";
          alternate.hreflang = tag;
          alternate.href = localizedURL(tag).href;
          document.head.append(alternate);
        });
        const defaultAlternate = document.createElement("link");
        defaultAlternate.rel = "alternate";
        defaultAlternate.hreflang = "x-default";
        defaultAlternate.href = localizedURL("en-US").href;
        document.head.append(defaultAlternate);

        const canonical = document.querySelector('link[rel="canonical"]');
        if (canonical) canonical.href = localizedURL(locale).href;

        if (updateAddress) window.history.replaceState(null, "", localizedURL(locale));
      };

      const requested = new URLSearchParams(window.location.search).get("lang");
      const initial = requested && isSupported(requested)
        ? requested
        : resolveLocale(navigator.languages?.[0] || navigator.language || "en-US");

      picker.addEventListener("change", () => setLocale(picker.value, true));
      setLocale(initial, false);
    })
    .catch((error) => console.error("HowLong page localization failed; English copy remains visible.", error));
})();
