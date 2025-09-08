async function addApp(name, icon, action) {
  const appContainer = document.getElementById("apps");
  if (document.getElementById(name)) {
    console.warn(`App with name ${name} already exists.`);
    return;
  }

  const success = await add_shortcut(name, action);
  if (!success) {
    console.error("Failed to add shortcut, app not created.");
    return;
  }

  const appDiv = document.createElement("div");
  appDiv.className = "app";
  appDiv.id = name;
  appDiv.onclick = async () => {
    try {
      const resp = await fetch("/execute_shortcut", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, action: action }),
      });
      const json = await resp.json();
      alert(`Actions: ${action.join(" + ")} | Status: ${json.status}`);
    } catch (err) {
      console.error(err);
    }
  };

  const img = document.createElement("img");
  img.src = icon;
  img.alt = name;

  const h4 = document.createElement("h4");
  h4.textContent = name;

  appDiv.appendChild(img);
  appDiv.appendChild(h4);
  appContainer.appendChild(appDiv);
}

async function add_shortcut(name, actions) {
  try {
    const response = await fetch("/settings/add_shortcut", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, actions }),
    });
    const data = await response.json();
    if (data.status === "success") {
      alert("Shortcut created successfully!");
      return true;
    } else {
      alert("Failed to create shortcut: " + data.message);
      return false;
    }
  } catch (error) {
    console.error("Error creating shortcut:", error);
    alert("Failed to create shortcut.");
    return false;
  }
}

function create_shortcut(name, actions) {
  fetch("/add_shortcut", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      actions: actions,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Shortcut created successfully!");
      add_shortcut_status = true;
    })
    .catch((error) => {
      console.error("Error creating shortcut:", error);
      alert("Failed to create shortcut.");
      add_shortcut_status = false;
    });
}

async function loadShortcuts() {
  try {
    const res = await fetch("/settings/list_shortcuts");
    const data = await res.json();

    if (data.status !== "success") return;

    const container = document.getElementById("apps");

    const shortcuts = data.shortcuts;

    for (const [name, actionsArray] of Object.entries(shortcuts)) {
      const appDiv = document.createElement("div");
      appDiv.className = "app";
      appDiv.id = name;

      // Formatage des actions : sépare les touches et enlève les espaces inutiles
      const actions = (
        Array.isArray(actionsArray) ? actionsArray : [actionsArray]
      ).map((s) => s.split(/\s+/).filter(Boolean));

      // Au clic : envoie la commande test au serveur
      appDiv.onclick = async () => {
        try {
          const resp = await fetch("/execute_shortcut", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ shortcut: name }),
          });
          const json = await resp.json();
        } catch (err) {
          console.error(err);
          alert("Erreur lors de l'exécution du raccourci");
        }
      };

      // Image selon le nom, fallback si elle n'existe pas
      const img = document.createElement("img");
      img.src = `/static/icons/${name}.png`; // ton dossier d'icônes
      img.alt = name;
      img.onerror = () => {
        img.src = "/static/images/default.png";
      };

      const h4 = document.createElement("h4");
      h4.textContent = name;

      appDiv.appendChild(img);
      appDiv.appendChild(h4);
      container.appendChild(appDiv);
    }
  } catch (err) {
    console.error("Erreur lors du chargement des raccourcis :", err);
  }
}

window.onload = async () => {
  await loadShortcuts();
  tsParticles.load("tsparticles", {
    background: {
      color: "#0d47a1",
    },
    particles: {
      number: {
        value: 80,
      },
      color: {
        value: "#ffffff",
      },
      shape: {
        type: "circle",
      },
      opacity: {
        value: 0.5,
      },
      size: {
        value: 3,
      },
      move: {
        enable: true,
        speed: 2,
      },
    },
  });
};
