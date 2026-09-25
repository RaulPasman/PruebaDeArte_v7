// Configuración de Prueba de Arte.
// webhookUrl: pegá entre las comillas la URL de tu Apps Script (termina en /exec).
//   Si queda vacía, la prueba funciona igual pero no guarda nada (útil para probar diseño).
// imagesBaseUrl: sólo hace falta si publicaste el sitio en algún lugar público (GitHub Pages,
//   Cloudflare Pages, etc.). Si la completás, el mail de resultado y el PDF muestran una
//   miniatura de cada obra en vez de sólo el texto. Tiene que apuntar a la carpeta
//   assets/artworks/ de tu sitio publicado, CON la barra final. Ejemplo:
//   "https://tu-usuario.github.io/prueba-de-arte/assets/artworks/"
//   Si queda vacía, el mail sigue funcionando normal, sólo que sin miniaturas.
window.PRUEBA_CONFIG = {
  webhookUrl: "",
  imagesBaseUrl: ""
};
