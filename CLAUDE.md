# Prueba de Arte (TestDeArte) — contexto del proyecto

Este archivo es para vos, Claude, al arrancar una sesión de Claude Code en este repo. Leelo
antes de tocar nada: evita que repitas errores ya encontrados y te da el estado real de avance,
no el que parece por encima mirando el código.

## Qué es esto

Una plataforma web (estática, sin backend propio) que hace un test de 24 duelos de obras +
preguntas, y devuelve un "perfil de mirada artística" (uno de 10 arquetipos). Es el primer
paso de un proyecto más grande (conexión con galerías, arte para el hogar, realidad aumentada),
pero **eso está fuera de alcance por ahora**. El foco actual es sólo: imágenes, motor de
perfiles, guardado de datos y curaduría, para llegar a un Friends & Family (F&F) con 20–40
personas.

Dueño del proyecto: Raúl, Head Trader en un broker-dealer argentino, sin background técnico.
Explicale las cosas en criollo, sin dar por sentado que sabe jerga de programación o de Google
Cloud. Trabajamos hasta ahora en español.

## Arquitectura

```
index.html, app.js, styles.css     → la app (vanilla JS, sin frameworks)
config.js                          → webhookUrl (Apps Script) e imagesBaseUrl (hosting público)
tracking.js                        → envía eventos a Apps Script (start/duel/question/result/feedback)
data/
  artworks.json                    → 60 obras, 8 ejes (E1..E8) cada una, -1..1
  duels.json                       → 16 duelos fijos + banco para 8 adaptativos
  profiles.json                    → 10 perfiles (P01..P09 + P10 "explorador sin fronteras" = fallback)
  scoring.json                     → pesos del motor, los lee score() en app.js
  questions.json                   → 7 preguntas con señales por eje
  image_sources.json               → de dónde sacar la imagen de cada obra (título de Wikipedia, etc.)
  image_manifest.json              → se genera solo, registro de qué imagen se bajó y de dónde
tools/fetch_images.py              → descarga imágenes de Wikimedia/Commons
apps_script/Code.gs                → receptor en Google Sheets + envío de mail con PDF
docs/                               → toda la documentación de decisiones y guías paso a paso
assets/artworks/                   → imágenes descargadas (.jpg)
assets/manual/                     → imágenes que Raúl carga a mano cuando el script no las encuentra
SIMULADOR_MOTOR.html               → corre miles de recorridos simulados para medir el motor de perfiles
REVISAR_IMAGENES.html              → se genera solo, grilla visual de las 60 imágenes
```

## Decisiones ya tomadas (no las reabras sin buena razón)

- **No se agregan funciones nuevas grandes** (realidad aumentada, cuentas de usuario, más de
  60 obras) hasta pasar el F&F con datos reales. Ver `docs/*roadmap*` si existe, o preguntale a
  Raúl.
- **Motor de perfiles (`app.js`, funciones `score()` / `profileResult()` / `prepararMotor_()`)**:
  reescrito para comparar la obra elegida contra la descartada (contraste), no promediar las
  obras elegidas. La versión vieja promediaba y convergía siempre hacia "El equilibrador"
  (93% de usuarios al azar caían ahí). La versión nueva usa distancia coseno contra vectores de
  perfil *centrados* (restando el promedio de los perfiles, no el del catálogo). Validado con
  `SIMULADOR_MOTOR.html`: 51% de acierto exacto, 87% contando perfil o matiz (el azar puro da
  11%). **Antes de tocar el motor, corré el simulador y compará el output contra estos
  números** — si algo baja, es una regresión.
  - Debilidad conocida: "El explorador de la materia" (P02) se confunde con "El buscador de
    intensidad" (P04) porque sus vectores están cerca. Si volvés a tocar `profiles.json`, tené
    esto en cuenta.
- **Imágenes (`tools/fetch_images.py`)**: usa la imagen principal del artículo de Wikipedia de
  cada obra (API `pageimages` con `pilicense=any` para traer también obras con derechos, en baja
  resolución). Detalles importantes:
  - Wikimedia sólo acepta miniaturas en tamaños estándar (1920px es el que usamos). Pedir un
    tamaño arbitrario (ej. 2400px) da HTTP 429.
  - Wikimedia Commons **no tiene** obras con derechos vigentes (Matisse, Dalí, Warhol, Kahlo,
    etc.) — no tiene sentido buscarlas ahí.
  - `manual_file()` en `fetch_images.py` busca por prefijo de ID sin importar la extensión real
    del archivo (Windows oculta extensiones por defecto: un archivo que se ve como "C04.jpg"
    puede en realidad llamarse "C04.jpg.jfif"). No asumas que un archivo en `assets/manual/`
    tiene la extensión que parece tener.
  - Encontramos al menos un error de datos serio: `J02` estaba cargada como "One and Three
    Shadows" cuando la obra real es "One and Three Chairs" (Kosuth). Ya corregido. Si algo no
    se encuentra y "no debería existir", dudá primero del dato antes de inventar una fuente.
  - **Nunca inventes una URL o nombre de archivo de Wikimedia/Commons sin verificarlo.** Ya pasó
    una vez (una URL de Commons para una foto de Atget que no existía) y costó tiempo de debug.
    Si tenés acceso a internet real (a diferencia de una sandbox sin salida), confirmá antes de
    escribir en `image_sources.json`.
  - Quedan obras sin resolver automáticamente (sin artículo propio en Wikipedia): revisar
    `docs/IMAGENES.md` para la lista y el estado actual.
- **Google Sheets (`apps_script/Code.gs`)**: puede correr como script vinculado a la planilla
  (`Extensions → Apps Script`) o standalone (`script.new` + `SHEET_ID` completado a mano). Si
  `SHEET_ID` está vacío y el script es standalone, todo falla en silencio — es el primer lugar
  para mirar si "no se guarda nada".
  - Para actualizar el código de un deployment ya publicado: **Deploy → Manage deployments →
    lápiz → Version: New version → Deploy**. Si en cambio se hace "New deployment", la URL
    cambia y hay que actualizar `config.js`.
- **Mail de resultado**: HTML cálido con tabla (compatible con clientes de mail), más un PDF
  adjunto generado con el truco `Utilities.newBlob(html, MimeType.HTML).getAs(MimeType.PDF)`
  (soporta HTML5 básico: tablas, bold, italic, links — no flexbox/grid, no fonts custom).
  Las miniaturas de las obras en el mail dependen de `imagesBaseUrl` en `config.js` apuntando a
  un hosting público (`docs/PUBLICAR_SITIO.md` explica cómo con GitHub Pages). Si
  `imagesBaseUrl` está vacío, cae a lista de texto sin romperse — no lo des por sentado roto si
  Raúl no publicó el sitio todavía.
- **Privacidad**: se recomienda GitHub Pages (público pero no indexado/no listado) sólo para el
  F&F. Para lanzamiento público hace falta resolver derechos de imagen de verdad (obra aportada
  por galerías/artistas) — no reproducir el esquema actual (Wikipedia/Commons) a mayor escala.

## Cómo probar sin romper nada

- **Motor de perfiles**: abrir `SIMULADOR_MOTOR.html` en un navegador (con un server local,
  `python3 -m http.server` desde la raíz del proyecto) y correr la simulación. Comparar contra
  los números de arriba (51% / 87%).
- **Descarga de imágenes**: `tools/fetch_images.py` — vos (Claude Code) SÍ tenés salida real a
  internet desde la máquina de Raúl, a diferencia de una sandbox sin red. Podés correrlo de
  verdad y ver qué pasa, no hace falta simular la API de Wikimedia como tuve que hacer yo.
- **Apps Script / Sheets**: no se puede probar desde acá ni desde Claude Code — vive en la
  cuenta de Google de Raúl. Para validar lógica de `Code.gs` sin tocar Sheets real, se puede
  mockear `SpreadsheetApp`/`MailApp`/`Utilities` en Node (hay un ejemplo de esto en el historial
  de chat, pedile a Raúl que te lo pase si lo necesitás, o reconstruilo: es un mock simple de
  objeto/hoja en memoria).

## Estado de avance (al 25 de septiembre de 2026)

**Resuelto y validado:**
- Motor de perfiles v2 (contraste) — implementado y validado por simulación. Falta validarlo
  con gente real en el piloto.
- Registro de datos en Sheets — funcionando de punta a punta.
- Encuesta de cierre (feedback) — funcionando.
- Mail cálido + PDF adjunto — funcionando, confirmado por Raúl.
- Las 60 obras tienen imagen: 38 OK, 15 en baja resolución (obras con derechos, ver
  `data/image_manifest.json`) y 7 cargadas a mano en `assets/manual/`.
- **Duelo en mobile**: la sección ocupa el alto de la ventana y las imágenes se achican para que
  las dos obras y los botones entren sin scrollear (verificado en 320×568, 360×640, 390×844 y
  compu). En celular se ocultan los textos de ayuda del duelo.
- **Guardado de progreso** (`save()` / `loadSaved()` / `restore()` en `app.js`): se guarda en
  `localStorage` del navegador de la persona. Al volver, la portada ofrece "Continuar donde quedé"
  o "Ver mi resultado". Retoma la misma `session_id`, así que en Sheets sigue siendo una sola
  fila. Se descarta si tiene más de 14 días o si referencia obras que ya no existen.
- **Volver al duelo anterior** (`goBack()`): botón "← Anterior" en el duelo. Descarta la última
  respuesta y manda un evento `back`. Las preguntas y pausas ya vistas no se repiten.
- **"No estoy seguro"** (choice `unsure`): cuenta como duelo respondido pero no suma señal.
- **Placeholder a ciegas**: en el duelo, ni el texto alternativo ni el aviso de imagen faltante
  muestran título o artista (sólo "Obra A" / "Obra B").
- **`scoring.json` unificado**: `score()` lee los pesos de ahí. Se cargaron los valores que ya
  usaba el código (los viejos del JSON eran otros y nunca se usaban). El simulador dio igual antes
  y después del cambio (~53% principal, ~86% principal o matiz, máx. 18% con usuarios al azar).
- **GitHub**: el repo `RaulPasman/PruebaDeArte_v7` ya es la fuente única; Raúl commitea desde
  GitHub Desktop (no hay `git` de línea de comandos instalado en su PC).

**A medio camino:**
- Imágenes en el mail vinculadas al perfil: código listo, falta que Raúl publique el sitio
  (GitHub Pages; al 25/09/2026 la URL `raulpasman.github.io/PruebaDeArte_v7` da 404) y complete
  `imagesBaseUrl`.
- `config.js` en el repo tiene `webhookUrl` vacío: sin eso, lo publicado en GitHub Pages no
  guarda nada en Sheets. Raúl tiene que pegar la URL `/exec` y commitear.
- `apps_script/Code.gs` cambió (etiqueta "No estoy seguro" en la hoja Eventos): hay que pegarlo en
  Apps Script y publicar como *New version* (ver arriba). Sin eso, esa columna queda vacía para
  esas respuestas; no rompe nada.
- 15 imágenes en baja resolución: decidir si se reemplazan antes del F&F (va con la curaduría).

**Pendiente — priorizar en este orden:**
1. **Curaduría 1.1**: aplicar los ~17 reemplazos de obras propuestos (ver conversación con
   Raúl o pedirle el PDF "Revisión Integral" que ya tiene), reclasificar familias, doble
   evaluación de vectores por dos personas. Bloqueado hasta tener ese PDF.
2. Recién después: **piloto moderado con 3–5 personas**, y más adelante el F&F completo.

**Cómo correr el simulador sin abrir el navegador a mano** (Edge viene con Windows):
armar un HTML con `<base href="file:///C:/.../PruebaDeArte_v7/">` que cargue `app.js` y repita la
lógica de `SIMULADOR_MOTOR.html`, y correrlo con
`msedge --headless=new --allow-file-access-from-files --virtual-time-budget=120000 --dump-dom <archivo>`.
Para capturas de celular, meter la página en un `<iframe>` de 390px: Edge headless no achica la
ventana por debajo de ~500px.

## Qué NO hacer

- No agregues dependencias/frameworks pesados — el proyecto es vanilla JS a propósito (simple,
  gratis de hostear, fácil de mantener por alguien no-técnico).
- No reestructurés archivos de datos (`artworks.json`, `profiles.json`, etc.) sin correr el
  simulador antes/después para confirmar que el motor sigue funcionando.
- No asumas que Raúl sabe qué es un deployment, un commit, un webhook, etc. — explicáselo en el
  momento, con pasos concretos y nombres exactos de botones.
