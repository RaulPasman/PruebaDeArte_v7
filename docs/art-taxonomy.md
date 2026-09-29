# Taxonomía artística (curaduría 2.0)

60 obras en 10 familias (26/09/2026). El prefijo del ID indica la familia. Entre paréntesis, el
valor exacto del campo `Familia` en `data/artworks.json`.

| Prefijo | Familia | Obras | Argentinas / internacionales |
|---|---|---|---|
| GE | Abstracción geométrica (`Geometric abstraction`) | 7 | 3 / 4 |
| CI | Arte cinético y óptico (`Kinetic / optical art`) | 5 | 3 / 2 |
| CF | Campo de color y abstracción atmosférica (`Color field / atmospheric abstraction`) | 5 | 1 / 4 |
| GS | Abstracción gestual (`Gestural abstraction`) | 5 | 3 / 2 |
| MA | Materia: textil, cerámica y escultura (`Material: textile, ceramic & sculpture`) | 8 | 4 / 4 |
| MC | Minimalismo cálido y formas orgánicas (`Warm minimalism & organic forms`) | 8 | 3 / 5 |
| FI | Figuración (`Figuration`) | 4 | 2 / 2 |
| FO | Fotografía (`Photography`) | 7 | 5 / 2 |
| PA | Paisaje (`Landscape`) | 3 | 1 / 2 |
| IM | Imaginario y surreal (`Imaginary / surreal`) | 5 | 3 / 2 |
| CO | Idea, objeto y pop (`Idea, object & pop`) | 3 | 2 / 1 |

Abstracción (GE+CI+CF+GS+MA+MC): 38 obras (~63%; MC incluye una foto y un mar de Richter).
Otros lenguajes: 22. Actualizado el 28/09/2026 (ver `docs/CURADURIA_2_0.md`, último ajuste). La familia MC se sumó el 26/09/2026: es el estilo "orgánico moderno" que
domina el arte para el hogar y el que más le gusta a Raúl.

Campos agregados en la 2.0: `Origen` (Argentina / Internacional) y `Fama` (1 = conocida en el
ambiente, 2 = conocida por quien sigue el arte, 3 = ícono). `Fama` la usa
`tools/armar_duelos.py` para que en cada duelo las dos obras sean parecidas en reconocimiento.

La familia se usa en el motor para dar variedad (duelos adaptativos, selección y recomendaciones
del resultado, paso "misma familia, otra voz" de la ruta); no se muestra al usuario. Lista
completa de obras en `docs/CURADURIA_2_0.md`.
