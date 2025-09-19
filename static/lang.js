let translations;

export function change_lang(lang) {
  return fetch(`/lang-get-${lang}`)
    .then((response) => response.json())
    .then((data) => {
      translations = data;
      localStorage.setItem("translations", JSON.stringify(data));
      update_lang();
      return data;
    });
}

export function update_lang() {
  if (!translations) return;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (translations[key]) {
      el.textContent = translations[key];
    }
  });
}

if (localStorage.getItem("lang")) {
  change_lang(localStorage.getItem("lang"));
} else {
  change_lang("en");
  localStorage.setItem("lang", "en");
}
