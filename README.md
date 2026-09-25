# TestDeArte / Prueba de Arte

Prototipo Friends & Family de TestDeArte: una experiencia visual para descubrir preferencias artísticas sin necesitar conocimientos previos.

## Ejecutar

Abrí el proyecto desde un servidor local (no directamente con `file://`):

```bash
python -m http.server 8000
```

Luego abrí `http://localhost:8000`.

## Qué incluye esta versión

- 60 obras con vectores de 8 ejes.
- 24 duelos: 16 fijos + 8 adaptativos.
- Respuestas A/B/Ambas/Ninguna.
- Pausas editoriales cada 4 duelos.
- 7 preguntas complementarias, incluida convivencia con una obra.
- Scoring ponderado y confianza por eje.
- 10 perfiles + perfil especial Explorador sin fronteras.
- Perfil principal + 2–3 matices.
- Cinco afinidades visuales sin números.
- Mi selección con diversidad.
- Recomendaciones con compatibilidad y expansión moderada.
- Penalización de recomendaciones demasiado parecidas a obras rechazadas.
- Contexto breve para las 60 obras mediante “mirá esto →”.
- Ruta guiada de 5 pasos.
- Exploración del artista cuando el catálogo ofrece obras adicionales.
- Reflexión final cualitativa.
- Pared visual personalizada.
- Vista preparada para guardar/imprimir en PDF.
- Responsive para desktop y mobile.
- Fallback visual si una imagen local/remota no carga.
- Herramientas para descargar y validar las 60 imágenes localmente.

## Estructura

```text
TestDeArte/
├── index.html
├── styles.css
├── app.js
├── data/
│   ├── artworks.json
│   ├── duels.json
│   ├── questions.json
│   ├── profiles.json
│   └── scoring.json
├── assets/artworks/
└── docs/
    ├── product-brief.md
    ├── functional-design.md
    ├── art-taxonomy.md
    ├── profile-system.md
    ├── testing-plan.md
    └── qa_checklist.md
```

## Imágenes

El proyecto soporta dos capas de imagen:

1. **archivo local** en `assets/artworks/ID.ext`;
2. **URL remota** de respaldo en `data/artworks.json`.

Si el archivo local existe, la app lo intenta primero. Si no está disponible, intenta la URL remota y, si también falla, muestra un placeholder sin romper el recorrido.

Para preparar una copia local de las 60 obras desde una máquina con Internet:

```bash
python tools/fetch_images.py
python tools/validate_images.py
```

También podés ejecutar `DESCARGAR_IMAGENES.bat` en Windows.

Las URLs actuales son candidatas de Wikimedia Commons/instituciones y deben validarse desde la red de hosting definitiva. La herramienta de descarga deja registrado qué archivos pudo obtener. Para publicación abierta conviene revisar además derechos/licencias de cada reproducción.

## F&F

Esta versión no contiene conexión comercial con galerías, artistas ni talleres. Esa capa queda deliberadamente fuera del prototipo actual.


## QA visual de imágenes
Ejecutá `VERIFICAR_IMAGENES.bat` para comprobar las 60 imágenes directamente desde el navegador y ver sus dimensiones.

## Estado v5 — F&F readiness

El producto está en etapa de preparación para Friends & Family. El motor y el recorrido están implementados; antes de compartirlo hay que validar las 60 imágenes desde la máquina donde se servirá la prueba y hacer un QA visual completo.

### Orden recomendado
1. Ejecutar `DESCARGAR_IMAGENES.bat`.
2. Ejecutar `VERIFICAR_IMAGENES.bat`.
3. Abrir `ABRIR_PRUEBA_DE_ARTE.bat`.
4. Completar el recorrido completo en desktop y móvil.
5. Generar el PDF.
6. Hacer un piloto con 3 personas.
7. Corregir cualquier bug antes de ampliar a F&F.

Ver `docs/FF_LAUNCH_CHECKLIST.md` y `docs/QA_V5.md`.

## Imágenes: paso previo obligatorio al lanzamiento F&F

Ejecutar `DESCARGAR_IMAGENES.bat`. Esta versión resuelve las obras contra Wikimedia Commons mediante la API en lugar de depender de nombres de archivo adivinados. Luego ejecutar `VERIFICAR_IMAGENES.bat`. No publicar en GitHub Pages hasta obtener 60/60 imágenes válidas.
