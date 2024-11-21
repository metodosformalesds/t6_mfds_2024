// landbot.js
let myLandbot;

export function initLandbot() {
  if (!myLandbot) {
    const s = document.createElement('script');
    s.type = 'text/javascript';
    s.async = true;
    s.addEventListener('load', function() {
      myLandbot = new Landbot.Livechat({
        configUrl: 'https://storage.googleapis.com/landbot.site/v3/H-2688657-D6A7FHN8HH99S74B/index.json',  // URL de configuración de tu bot
      });
    });
    s.src = 'https://cdn.landbot.io/landbot-3/landbot-3.0.0.js';  // URL de la fuente del script de Landbot
    const x = document.getElementsByTagName('script')[0];
    x.parentNode.insertBefore(s, x);
  }
}

// Añadir los event listeners
window.addEventListener('mouseover', initLandbot, { once: true });
window.addEventListener('touchstart', initLandbot, { once: true });
