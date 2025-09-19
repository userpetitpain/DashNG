let translations;

function change_lang(lang) {
  fetch(`/api/get-${lang}`)
    .then((response) => response.json())
    .then((data) => {
      translations = data;
      update_lang();
    });
}

function update_lang(lang) {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    el.textContent = translations[lang][key];
  });
}

window.onload = () => {
  if (localStorage.getItem("lang")) {
    change_lang(localStorage.getItem("lang"));
  } else {
    change_lang("en");
  }
};
