const settings_popup = document.getElementById("settings_popup");

const show_popup = (p) => {
  p.style.display = 'block';
  p.classList.add('y-fade-in');
  p.classList.remove('fade-out');
}

const hide_popup = (p) => {
  p.classList.add('fade-out');
  p.classList.remove('y-fade-in');
  p.addEventListener('animationend', () => {
    p.style.display = 'none';
  }, { once: true });
}

// Exemple : clic sur un bouton pour ouvrir/fermer
document.getElementById("settings").onclick = () => show_popup(settings_popup);
settings_popup.onclick = () => hide_popup(settings_popup);
