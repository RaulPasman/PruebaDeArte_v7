# Testing plan — Friends & Family

## QA funcional
- Carga desde servidor local.
- Intro → identidad → duelo.
- A/B/Ambas/Ninguna registran respuesta.
- No hay retroceso.
- Pausas cada 4 duelos.
- Las preguntas aparecen después de la pausa correspondiente.
- La pregunta de convivencia muestra una obra cuando existe una elección directa reciente.
- Se completan 24 duelos y 7 preguntas.
- El resultado aparece una sola vez y no expone puntajes internos.
- Mi selección sólo contiene obras ya vistas.
- Las recomendaciones no repiten obras vistas.
- La ruta tiene cinco pasos y termina en reflexión.
- Volver al resultado conserva el resultado.
- Reiniciar devuelve el producto al inicio.
- Print/Guardar genera la vista preparada para PDF.

## QA visual
- Desktop ancho: 1280–1600 px.
- Laptop: 1024–1280 px.
- Mobile: 390–430 px.
- Verificar que las imágenes mantengan proporción.
- Verificar fallback cuando una imagen remota falla.
- Verificar contraste y foco de teclado.

## QA de contenido
- Revisar títulos, artistas y años antes de publicación abierta.
- Revisar especialmente obras contemporáneas con derechos de reproducción.
- Validar cada URL de imagen y resolución objetivo ≥1200 px.
- Revisar que los textos de contexto no suenen a diagnóstico ni a clase académica.
