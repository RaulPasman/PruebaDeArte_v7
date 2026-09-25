# Prueba de Arte — v3

## Correcciones
- Q06 ahora se muestra correctamente después del duelo 22; antes su condición existía en datos pero el flujo sólo disparaba preguntas en las pausas de cada 4 duelos.
- La reflexión final se conserva y se muestra en el cierre del resultado.
- J02 fue normalizada como **One and Three Shadows [Ety./Hist.]**, 1965, de Joseph Kosuth.

## Imágenes
- Cada obra tiene `image_file` para una copia local.
- La aplicación intenta primero el archivo local y luego la URL remota.
- Si ambas fallan, aparece un placeholder sin romper el duelo.
- Se agregaron `tools/fetch_images.py` y `tools/validate_images.py`.
- En Windows se puede usar `DESCARGAR_IMAGENES.bat`.

## QA
- `validate.py`: 60 obras / 24 duelos / 10 perfiles / 7 preguntas / 8 ejes.
- `node --check app.js`: OK.
- `qa_flow.py`: OK; las 7 preguntas son alcanzables.
