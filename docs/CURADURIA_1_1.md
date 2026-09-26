# Curaduría 1.1

Basada en la Revisión Integral (sección 3). Estado al 25/09/2026:

- **Hecho:** los 17 reemplazos aplicados, con imagen; familias reclasificadas (13, ver
  `docs/art-taxonomy.md`); ya no hay obras duplicadas; todas las obras entran en algún duelo
  (banco adaptativo de 16 duelos, recalculado con los vectores nuevos); textos propios por perfil.
- **Simulador con el catálogo final:** ~59–60% perfil principal, ~88% principal o matiz
  (objetivo de la revisión: ≥60% / ≥85%).
- **Falta:** la doble evaluación de los vectores (paso 2). Los vectores de las 17 obras nuevas
  son borrador de IA.

## Paso 1 · Obras que entraron (hecho)

| ID | Sale | Entra | Imagen tomada de |
|----|------|-------|------------------|
| A04 | Malevich, *Suprematist Composition* | Hilma af Klint, *The Ten Largest, No. 7, Adulthood* (1907) | Wikimedia Commons (dominio público) |
| B06 | Matisse, *La danza* | Xul Solar, *Drago* (1927) | WikiArt |
| C04 | Velázquez, *Las Meninas* | Antonio Berni, *Manifestación* (1934) | WikiArt |
| C05 | Vermeer, *La joven de la perla* | David Hockney, *A Bigger Splash* (1967) | Wikipedia (baja resolución) |
| D03 | Friedrich, *El caminante* | Hiroshi Sugimoto, *Seascape: Aegean Sea, Pillon* (1990) | WikiArt |
| D04 | Constable, *The Hay Wain* | Etel Adnan, *Mount Tamalpais* (1985) | WikiArt |
| E07 | Lumière (film) | Saul Leiter, *Red Umbrella* (c. 1958) | artblart.com |
| F01 | Miguel Ángel, *David* | Alexander Calder, *Lobster Trap and Fish Tail* (1939) | WikiArt |
| F02 | Rodin, *El pensador* | Gyula Kosice, *Deformación de la gota circunvalada* (1965) | WikiArt |
| F05 | Bernini, *Apolo y Dafne* | Ruth Asawa, *Untitled (S.270)* (1955) | Whitney Museum |
| G07 | Pollock, *Blue Poles* | Sheila Hicks, *Grand Prayer Rug* (1966) | WikiArt |
| H05 | Duchamp, *L.H.O.O.Q.* | Rogelio Polesello, *Sin título* (1959) | MALBA |
| I03 | Yoko Ono, *Cut Piece* | Lucio Fontana, *Concetto spaziale, Attesa* (1966) | WikiArt |
| I04 | Hirst, el tiburón | Liliana Porter, *Diálogo (con pingüino)* (1998) | Museo Reina Sofía |
| J02 | Kosuth (duplicada con I02) | Jorge Macchi, *Buenos Aires Tour* (2003) | jorgemacchi.com |
| J04 | Cindy Sherman, *Film Still #35* | Carlos Cruz-Diez, *Physichromie No. 326* (1967) | WikiArt |
| J05 | Smithson, *Spiral Jetty* | Julio Le Parc, *Continuel Mobile Lumière* (1968) | WikiArt |

Las imágenes están en `assets/manual/` (salvo A04 y C05, que baja `fetch_images.py`). Son
imágenes de obras con derechos, usadas para una prueba privada; antes de una versión pública
hay que reemplazarlas por imágenes con permiso (ver Revisión Integral, sección 6).

Si alguna no te convence, guardá otra imagen con el mismo nombre en `assets/manual/`, cambiá
título y año en `data/curaduria_1_1.json` y pedime que la vuelva a aplicar
(`python tools/aplicar_curaduria.py --ids ID` y `python tools/fetch_images.py --only ID --force`).

Algunas imágenes quedaron chicas (menos de 600 px: Xul Solar, Berni, Sugimoto, Adnan, Hicks,
Macchi, Cruz-Diez, Le Parc, Hockney). En el celular se ven bien; en una compu grande pueden verse
algo blandas.

## Paso 2 · Doble evaluación de los vectores

Los 8 valores de cada obra los asignó una IA. La revisión recomienda que los asignen **dos
personas por separado** (vos y alguien del mundo del arte) para detectar desacuerdos.

1. La planilla está en `docs/evaluacion/plantilla_vectores.csv` (se regenera con
   `python tools/evaluacion_vectores.py plantilla`).
2. Cada uno la abre en Excel o Google Sheets, completa los 8 valores de cada obra **sin mirar
   los del otro ni los actuales**, y la guarda como CSV con otro nombre.
3. Me pasás los dos archivos: los comparo, marcamos los ejes donde difieren en más de 0,5, los
   discuten, y con el resultado actualizo `artworks.json` y corro el simulador.

### Qué significa cada eje (de -1 a 1)

| Eje | -1 | +1 | Pregunta para decidir |
|-----|----|----|-----------------------|
| E1 | Abstracto | Figurativo | ¿Se reconocen personas, objetos o lugares? |
| E2 | Estructurado | Espontáneo | ¿Está planificado y ordenado, o se ve libre y gestual? |
| E3 | Sereno | Expresivo | ¿Transmite calma o intensidad emocional? |
| E4 | Contenido | Saturado | ¿Poco color y pocos elementos, o mucho de todo? |
| E5 | Plano | Material | ¿Superficie lisa y plana, o textura, relieve, volumen? |
| E6 | Cotidiano | Imaginario | ¿Muestra el mundo real o uno inventado / simbólico? |
| E7 | Íntimo | Dominante | ¿Es una obra para mirar de cerca, o se impone en el espacio? |
| E8 | Transparente | Conceptual | ¿Se entiende con los ojos, o hace falta pensar la idea detrás? |

Sobre **E7**: en las obras originales ninguna tiene valor negativo, así que en la práctica el eje
casi no distingue. Al evaluar, usá toda la escala: una acuarela chica o una foto íntima deberían
ir claramente hacia -1.

Duelos fijos todavía flojos (las dos obras se parecen mucho en los vectores actuales): **D10**
(Hopper vs Atget) y **D16** (Lange vs Wyeth). Conviene revisarlos después de la doble evaluación.
