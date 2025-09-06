window.onload = async () => {
  tsParticles.load("tsparticles", {
    background: {
      color: "#0d1117",
    },
    particles: {
      number: { value: 80 },
      size: { value: 3 },
      color: { value: "#ffffff" },
      move: { enable: true, speed: 2 },
      links: {
        enable: true,
        distance: 150,
        color: "#ffffff",
        opacity: 0.4,
        width: 1,
      },
    },
    interactivity: {
      events: {
        onHover: { enable: true, mode: "repulse" },
        onClick: { enable: true, mode: "push" },
      },
      modes: {
        repulse: { distance: 100 },
        push: { quantity: 4 },
      },
    },
  });
};

const fullscreenBTN = document.getElementById("fullscreenbutton");

fullscreenBTN.addEventListener("click", () => {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    document.documentElement.requestFullscreen();
  }
});

function updateDateTime() {
  const now = new Date();

  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  document.getElementById(
    "time"
  ).textContent = `${hours}:${minutes}:${seconds}`;

  const day = String(now.getDate()).padStart(2, "0");
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const year = now.getFullYear();
  document.getElementById("date").textContent = `${day}/${month}/${year}`;
}
setInterval(updateDateTime, 1000);
updateDateTime();

let battery_level = Math.floor(Math.random() * 100) + 1;
let charging = false;

const battery = document.getElementById("battery");
const charging_icon = document.getElementById("charging");

function update_battery() {
  if (!charging) {
    battery_level -= 1;
  } else {
    battery_level += 1;
  }

  if (battery_level > 85)
    battery.src = "static/images/battery-full-solid-full.svg";
  else if (battery_level > 45)
    battery.src = "static/images/battery-half-solid-full.svg";
  else if (battery_level > 10)
    battery.src = "static/images/battery-quarter-solid-full.svg";
  else
    battery.src = "static/images/battery-empty-solid-full.svg";

  if (charging || battery_level < 2) {
    charging_icon.style.display = "inline-block";
    charging = true;
  } else {
    charging_icon.style.display = "none";
  }

  if (battery_level <= 2) charging = true;
  if (battery_level >= 100) charging = false;
}


setInterval(update_battery, 2000);
update_battery();
