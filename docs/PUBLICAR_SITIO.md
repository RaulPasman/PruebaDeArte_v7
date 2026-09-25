# Publicar el sitio (para que el mail muestre imágenes de las obras)

Esto es opcional. Sin esto, el mail y el PDF funcionan igual, sólo que con la lista de obras
en texto en vez de con miniaturas. Es el mismo paso de "hosting" que ya estaba planeado para
antes del F&F, así que no es trabajo extra — sólo lo estás haciendo ahora en vez de más
adelante.

## Por qué hace falta
Las imágenes de las obras están en tu computadora (`assets/artworks/`). Para que el mail
—que lo recibe otra persona, en otra PC— pueda mostrarlas, tienen que estar en algún lugar de
internet accesible por URL. GitHub Pages es gratis y anda bien para esto.

## Pasos (GitHub Pages)
1. Si no tenés cuenta de GitHub, creá una en https://github.com/join (gratis).
2. Creá un repositorio nuevo: botón **New** → nombre, por ejemplo `prueba-de-arte` → marcalo
   **Private** si querés (igual va a ser visible por quien tenga el link, ver nota abajo) →
   **Create repository**.
3. Subí la carpeta completa del proyecto a ese repositorio. Lo más simple: instalá
   **GitHub Desktop** (https://desktop.github.com), "Add local repository", elegí la carpeta
   del proyecto, y "Publish repository".
4. En GitHub, andá a **Settings → Pages** (del repositorio, no de tu cuenta).
5. En **Source**, elegí **Deploy from a branch**, rama **main**, carpeta **/ (root)** →
   **Save**.
6. Esperá 1–2 minutos. GitHub te va a mostrar una URL como:
   `https://tu-usuario.github.io/prueba-de-arte/`

## Nota sobre privacidad
GitHub Pages publica el sitio en una URL pública. No aparece en buscadores ni se comparte con
nadie que no tenga el link (nadie lo va a encontrar buscando en Google), pero técnicamente
cualquiera que tenga la URL puede entrar. Para un F&F esto es un riesgo bajo y así está
contemplado en la revisión del proyecto. Si en algún momento querés restringirlo más, se
puede mover a un hosting con contraseña (lo vemos llegado el caso).

## Conectar las imágenes al mail
1. Copiá tu URL de GitHub Pages y agregale `assets/artworks/` al final:
   `https://tu-usuario.github.io/prueba-de-arte/assets/artworks/`
2. Abrí `config.js` y pegala en `imagesBaseUrl`:
   ```js
   window.PRUEBA_CONFIG = {
     webhookUrl: "...",
     imagesBaseUrl: "https://tu-usuario.github.io/prueba-de-arte/assets/artworks/"
   };
   ```
3. Guardá y volvé a subir ese archivo al repositorio (con GitHub Desktop: "Commit" → "Push").
4. Hacé el test de nuevo: el mail y el PDF ahora deberían traer una miniatura de cada obra de
   tu selección y de las recomendadas.

## Si más adelante cambiás imágenes o agregás obras
Cada vez que cambies algo en la carpeta del proyecto, tenés que volver a subirlo a GitHub
(Commit → Push) para que el sitio publicado se actualice. GitHub Desktop te va a mostrar qué
cambió antes de subirlo.
