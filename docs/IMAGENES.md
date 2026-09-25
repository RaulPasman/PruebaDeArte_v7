# Imágenes — procedimiento (v7)

## Por qué falló la v6 (11 OK / 49 error)
1. **Tamaño de miniatura no estándar.** Desde 2026 Wikimedia rechaza con HTTP 429 las miniaturas que no usan sus tamaños estándar (20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840 px). La v6 pedía 2400 px.
2. **Demasiadas llamadas sin identificarse.** ~5 búsquedas por obra, User-Agent genérico, sin esperar ante un 429. A partir de la obra 9 Wikimedia bloqueó todo.
3. **Buscar en Commons no sirve para obras con derechos.** Commons no aloja Pollock, Matisse, Dalí, Magritte, Warhol, Kahlo, Wyeth, Sherman, etc. Además, la búsqueda por texto trajo imágenes equivocadas (p. ej. C04 = un *detalle* de Las Meninas; C01 = un archivo de 13 KB).

## Cómo funciona la v7
- Toma la **imagen principal del artículo de Wikipedia** de cada obra (definida en `data/image_sources.json`).
- Agrupa hasta 50 obras por llamada: ~10–20 llamadas de API en total en vez de ~300.
- Pide miniaturas de **1920 px** y guarda JPG de **1600 px** (≈250–600 KB).
- Reintenta con espera progresiva y respeta `Retry-After`.
- Es **reanudable**: si se corta, se vuelve a ejecutar y sigue.
- No toca `data/artworks.json`; registra todo en `data/image_manifest.json`.
- Genera `REVISAR_IMAGENES.html` para control visual.

## Pasos
1. Abrir `tools/fetch_images.py` y reemplazar `completar-tu-mail@ejemplo.com` por tu mail (línea `CONTACTO`).
2. Doble clic en `DESCARGAR_IMAGENES.bat` (instala Pillow solo si falta).
3. Revisar `REVISAR_IMAGENES.html`: que cada imagen sea la obra completa y correcta.
4. Si alguna falta o está mal: guardar la imagen correcta como `assets/manual/ID.jpg` y volver a ejecutar.

## Estados
- **OK**: imagen ≥ 700 px.
- **LOW_RES**: obra con derechos; Wikipedia sólo publica una versión chica. Sirve para miniaturas; para el duelo conviene reemplazarla manualmente o cambiar la obra.
- **MANUAL**: imagen provista por vos en `assets/manual/`.
- **MISSING / ERROR**: sin imagen.

## Obras que casi seguro requieren acción manual
- **J02** (Kosuth, *One and Three Shadows*): no pudimos confirmar que la obra exista con ese título. Recomendación: reemplazarla.
- **E03 / J04** (Cindy Sherman, *Film Stills* #21 y #35): no tienen artículo propio; conseguir imagen a mano o reemplazar una.
- Obras con derechos vigentes (Pollock, Matisse, Dalí, Magritte, Warhol, Kahlo, Wyeth, Hopper, Chagall, Hirst…) probablemente salgan en **baja resolución**.

## Actualización v7.2 · si "vuelve a pedir" una imagen que ya cargaste a mano

Causa casi segura: **Windows tiene ocultas las extensiones de archivo**, así que al renombrar
`imagen.jfif` (o `.jpge`, `.webp`, etc.) a `C04.jpg`, en realidad el archivo queda guardado como
`C04.jpg.jfif` — vos ves "C04.jpg" en el Explorador, pero el nombre real tiene la extensión vieja
pegada atrás, y el script no lo reconoce.

**Cómo confirmarlo:** en el Explorador de Windows, `Vista → Extensiones de nombre de archivo`
(casilla). Ahora vas a ver el nombre real de cada archivo dentro de `assets/manual/`.

**Ya no hace falta corregirlo a mano:** desde esta versión, `fetch_images.py` busca cualquier
archivo que *empiece* con el ID de la obra, sin importar qué extensión tenga pegada atrás, y
comprueba que sea una imagen válida antes de usarlo. Si de todas formas una obra sigue sin
resolverse, correr el .bat ahora imprime un aviso como:

```
AVISO: en assets/manual/ hay archivos que no coinciden con ningún ID de obra:
   - H2.jpg  (¿nombre mal escrito? tiene que empezar con el ID exacto, ej: C04...)
```

Eso avisa si el nombre está mal escrito (por ejemplo `H2.jpg` en vez de `H02.jpg`).

## E05 (Eugène Atget) — por qué no aparece sola

Atget no tiene un artículo propio en Wikipedia para ninguna foto puntual (a diferencia de "La
noche estrellada" o "El grito"), así que el buscador automático no la puede resolver sola. Toda
su obra es de dominio público (murió en 1927), así que cualquier imagen sirve:

1. Andá a https://commons.wikimedia.org/w/index.php?search=Atget+Paris+street&title=Special:MediaSearch
2. Elegí cualquier foto de calle que te guste (todas son de dominio público).
3. Descargala y guardala como `assets/manual/E05.jpg`.
4. Volvé a correr `DESCARGAR_IMAGENES.bat`.

Si preferís no complicarte, decime y la sacamos del test junto con los otros reemplazos
propuestos en la revisión (es justamente el tipo de obra difícil de conseguir que esa lista busca evitar).

## Actualización v7.3 · 5 obras encontradas y corregidas

Reviisé una por una las 9 obras que seguían sin resolverse. Dos se arreglaron solas:

- **G01** (Matisse, "The Snail"): el título de Wikipedia estaba mal buscado. Ya corregido.
- **J02** (Kosuth): el dato tenía el título mal cargado — decía "One and Three Shadows",
  cuando la obra real (y muy famosa) es **"One and Three Chairs"** (una silla, la foto de esa
  silla, y la definición de diccionario de "silla"). Ya corregido en `artworks.json` y en el
  buscador; se resuelve sola.

Las otras 5 no tienen un artículo propio en Wikipedia (a diferencia de La noche estrellada, cada
una de estas obras sólo aparece mencionada dentro de la biografía del artista, sin imagen
dedicada), así que no hay forma automática y confiable de bajarlas. Guardalas a mano en
`assets/manual/` con estos links de búsqueda:

| ID | Obra | Buscar en |
|----|------|-----------|
| E05 | Atget, calle de París (cualquiera) | https://commons.wikimedia.org/w/index.php?search=Atget+Paris+street&title=Special:MediaSearch |
| G03 | Schwitters, collage sin título | https://commons.wikimedia.org/w/index.php?search=Kurt+Schwitters+collage&title=Special:MediaSearch |
| G04 | Höch, "Cut with the Kitchen Knife" | https://commons.wikimedia.org/w/index.php?search=Hannah+H%C3%B6ch+kitchen+knife&title=Special:MediaSearch |
| G05 | Schwitters, "Merzbild 32A" | https://www.moma.org/collection/works/?query=Schwitters%20Merzbild |
| J01 | Judd, "Untitled (Stack)" | https://www.google.com/search?q=Donald+Judd+Untitled+Stack+1967&tbm=isch |
| J03 | Nevelson, "Sky Cathedral" | https://www.moma.org/collection/works/81006 (imagen educativa, mismo criterio que las demás) |
| J04 | Sherman, "Untitled Film Still #35" | ya está en la lista de reemplazos propuestos; si preferís no buscarla, decime y la sacamos del test |

Las cuatro primeras (G03, G04, G05, J01) son de dominio público o de circulación educativa
libre: cualquier imagen que encuentres sirve, no hace falta que sea "la" foto oficial. Guardalas
como `assets/manual/G03.jpg`, `assets/manual/G04.jpg`, etc. y volvé a correr el .bat.
