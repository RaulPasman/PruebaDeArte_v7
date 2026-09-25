# QA v5

## Estructura
- 60 obras
- 24 duelos
- 10 perfiles
- 7 preguntas
- 8 ejes
- 44 artistas

## Reglas verificadas
- Sin referencias de duelo inválidas.
- Sin duelos duplicados.
- Q01/Q02/Q03/Q04/Q05/Q06/Q07 aparecen en 4/8/12/16/20/22/24.
- Todas las obras tienen `image_url` e `image_file`.
- El loader intenta imagen local primero y URL remota como fallback.
- El placeholder no bloquea el recorrido si una imagen falla.
- `node --check app.js` OK.

## Limitación conocida
La descarga HTTP de las imágenes no puede completarse desde el entorno de desarrollo actual por falta de resolución de red. Debe ejecutarse `DESCARGAR_IMAGENES.bat` o `VERIFICAR_IMAGENES.bat` en una máquina con Internet antes del F&F.
