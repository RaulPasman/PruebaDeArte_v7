# Taxonomía artística del MVP

60 obras distribuidas en 12 familias (reclasificadas el 25/09/2026 según la Revisión Integral,
sección 3: había obras en familias que no les correspondían). Entre paréntesis, el nombre exacto
del campo `Familia` en `data/artworks.json`.

1. Abstracción geométrica (`Geometric abstraction`) — 6: A01–A06
2. Abstracción gestual (`Gestural / expressive abstraction`) — 4: B02, B03, B04, G07
3. Expresionismo / figuración expresiva (`Expressionism / expressive figuration`) — 3: B01, B05, B06
4. Figuración / realismo (`Figuration / realism`) — 5: C01–C05
5. Surrealismo / imaginario (`Surrealism / imaginary`) — 5: C06, C07, G02, H01, H02
6. Paisaje y atmósferas (`Landscape / atmosphere`) — 5: D01–D04, D06
7. Fotografía artística (`Artistic photography`) — 9: D05, E01–E07, J04
8. Escultura y objetos (`Sculpture / object`) — 6: F01–F06
9. Textil, collage y técnica mixta (`Textile / collage / mixed media`) — 5: G01, G03–G06
10. Gráfica, grabado y pop (`Graphic / print / pop`) — 4: H03–H06
11. Arte conceptual accesible (`Accessible conceptual art`) — 4: I01–I04
12. Minimalismo, objeto e ideas (`Minimalism / object / ideas`) — 4: J01, J02, J03, J05

La letra del ID (A, B, C…) ya no indica la familia: se mantuvo para no romper duelos, imágenes ni
datos guardados. La familia se usa en el motor para dar variedad (duelos adaptativos, selección y
recomendaciones del resultado, paso "misma familia, otra voz" de la ruta), no se muestra al usuario.

Cada obra contiene un vector de ocho ejes, metadatos básicos y un texto breve de observación. Los
textos de contexto priorizan qué mirar antes que una explicación académica extensa.

Los reemplazos de la curaduría 1.1 (17 obras) están en `docs/CURADURIA_1_1.md`; cuando entren,
cada obra nueva trae su familia de esta lista, más una familia 13 nueva: **Arte cinético y
óptico** (`Kinetic / optical art`) para Polesello (H05), Cruz-Diez (J04) y Le Parc (J05).
