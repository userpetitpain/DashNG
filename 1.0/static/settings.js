const list_shortcuts = () => {
  fetch('/settings/list_shortcuts')
    .then(res => res.json())
    .then(data => {
      if (data.status !== "success") return;

      const container = document.querySelector("ul")
      container.innerHTML = '';

      const shortcuts = data.shortcuts;

      for (const [nom, action] of Object.entries(shortcuts)) {
        const btn = document.createElement('button');
        btn.textContent = nom;
        btn.onclick = () => {
          alert(`Action : ${action}`); // ici tu peux envoyer la requête POST
        };
        const li = document.createElement("li");
        li.appendChild(btn);
        container.appendChild(li);
      }
    })
    .catch(err => console.error("Erreur :", err));
  }

add_shortcut_status = false

async function addApp(name, icon, action) {
  const appContainer = document.getElementById('apps');
  if (document.getElementById(name)) {
    console.warn(`App with name ${name} already exists.`);
    return;
  }

  const success = await add_shortcut(name, action);
  if (!success) {
    console.error("Failed to add shortcut, app not created.");
    return;
  }

  const appDiv = document.createElement('div');
  appDiv.className = 'app';
  appDiv.id = name;
  appDiv.onclick = action;

  const img = document.createElement('img');
  img.src = icon;
  img.alt = name;

  const h4 = document.createElement('h4');
  h4.textContent = name;

  appDiv.appendChild(img);
  appDiv.appendChild(h4);
  appContainer.appendChild(appDiv);
}

async function add_shortcut(name, actions) {
  try {
    const response = await fetch('/settings/add_shortcut', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, actions: actions })
    });
    const data = await response.json();
    if (data.status === "success") {
      alert("Shortcut created successfully!");
      return true;
    } else {
      alert("Failed to create shortcut.");
      return false;
    }
  } catch (error) {
    console.error("Error creating shortcut:", error);
    alert("Failed to create shortcut.");
    return false;
  }
}

function remove_shortcut(name) {
  fetch('/settings/remove_shortcut', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === "success") {
      const appDiv = document.getElementById(name);
      if (appDiv) {
        appDiv.remove();
      }
      alert("Shortcut removed successfully!");
    } else {
      alert("Failed to remove shortcut. >:)");
    }
  })
  .catch(error => {
    console.error("Error removing shortcut:", error);
    alert("Failed to remove shortcut.");
  });
}

window.onload = list_shortcuts;