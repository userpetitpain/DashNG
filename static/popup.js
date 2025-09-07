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