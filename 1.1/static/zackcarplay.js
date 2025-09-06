window.onload = async () => {
  
  
  tsParticles.load("tsparticles", {
    background: {
      color: "#0d1117"
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
        width: 1
      }
    },
    interactivity: {
      events: {
        onHover: { enable: true, mode: "repulse" },
        onClick: { enable: true, mode: "push" }
      },
      modes: {
        repulse: { distance: 100 },
        push: { quantity: 4 }
      }
    }
  });
}