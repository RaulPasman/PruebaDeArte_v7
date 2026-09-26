# Taxonomía artística (curaduría 2.0)

60 obras en 10 familias (26/09/2026). El prefijo del ID indica la familia. Entre paréntesis, el
valor exacto del campo `Familia` en `data/artworks.json`.

| Prefijo | Familia | Obras | Argentinas / internacionales |
|---|---|---|---|
| GE | Abstracción geométrica (`Geometric abstraction`) | 8 | 4 / 4 |
| CI | Arte cinético y óptico (`Kinetic / optical art`) | 5 | 3 / 2 |
| CF | Campo de color y abstracción atmosférica (`Color field / atmospheric abstraction`) | 4 | 1 / 3 |
| GS | Abstracción gestual (`Gestural abstraction`) | 7 | 3 / 4 |
| MA | Materia: textil, cerámica y escultura (`Material: textile, ceramic & sculpture`) | 11 | 6 / 5 |
| FI | Figuración (`Figuration`) | 7 | 4 / 3 |
| FO | Fotografía (`Photography`) | 6 | 3 / 3 |
| PA | Paisaje (`Landscape`) | 3 | 1 / 2 |
| IM | Imaginario y surreal (`Imaginary / surreal`) | 5 | 3 / 2 |
| CO | Idea, objeto y pop (`Idea, object & pop`) | 4 | 2 / 2 |

Abstracción (GE+CI+CF+GS+MA): 35 obras (58%). Otros lenguajes: 25.

Campos agregados en la 2.0: `Origen` (Argentina / Internacional) y `Fama` (1 = conocida en el
ambiente, 2 = conocida por quien sigue el arte, 3 = ícono). `Fama` la usa
`tools/armar_duelos.py` para que en cada duelo las dos obras sean parecidas en reconocimiento.

La familia se usa en el motor para dar variedad (duelos adaptativos, selección y recomendaciones
del resultado, paso "misma familia, otra voz" de la ruta); no se muestra al usuario. Lista
completa de obras en `docs/CURADURIA_2_0.md`.
