# Curaduría 1.1 — cómo terminarla

Basada en la Revisión Integral (sección 3). Estado al 25/09/2026:

- **Hecho:** familias reclasificadas (ver `docs/art-taxonomy.md`); **A04** (Hilma af Klint) y
  **C05** (Hockney) ya reemplazadas, con imagen; todas las obras entran en algún duelo (banco
  adaptativo de 16 duelos); textos propios por perfil. Simulador: ~61% perfil principal, ~92%
  principal o matiz (objetivo de la revisión: ≥60% / ≥85%).
- **Falta (de tu lado):** elegir la obra puntual y conseguir la imagen de las 15 restantes, y la
  doble evaluación de los vectores.

## Paso 1 · Las 15 imágenes

Estas obras tienen derechos de autor vigentes y no tienen artículo propio en Wikipedia, así que
no hay forma automática de bajarlas: hay que elegirlas y guardarlas a mano. Para cada una:

1. Abrí el link de búsqueda, elegí **una obra concreta** que te guste (que sea la obra completa,
   no una foto de sala ni un detalle) y anotá el **título y el año** que figuran en la fuente
   (museo, galería o fundación).
2. Guardá la imagen en `assets/manual/` con el ID como nombre: por ejemplo `B06.jpg`. Mejor si
   mide 1000 px o más del lado largo.
3. Pasame la lista de títulos y años: yo completo los datos, aplico los reemplazos, proceso las
   imágenes y corro el simulador.

| ID | Sale | Entra | Qué buscar | Buscar en |
|----|------|-------|------------|-----------|
| B06 | Matisse, *La danza* | **Xul Solar** | Una acuarela chica con símbolos, letras y figuras | [buscar](https://www.google.com/search?tbm=isch&q=Xul+Solar+acuarela) |
| C04 | Velázquez, *Las Meninas* | **Antonio Berni**, *Manifestación* (1934) | Ya está elegida: sólo falta la imagen (MALBA) | [buscar](https://www.google.com/search?tbm=isch&q=Antonio+Berni+Manifestaci%C3%B3n+1934) |
| D03 | Friedrich, *El caminante* | **Hiroshi Sugimoto**, serie *Seascapes* | Una foto de mar con el horizonte al medio | [buscar](https://www.google.com/search?tbm=isch&q=Hiroshi+Sugimoto+Seascapes) |
| D04 | Constable, *The Hay Wain* | **Etel Adnan** | Un óleo chico de paisaje, bloques de color | [buscar](https://www.google.com/search?tbm=isch&q=Etel+Adnan+painting+Mount+Tamalpais) |
| E07 | Lumière (es un film) | **Saul Leiter** | Una foto color de Nueva York, años 50 | [buscar](https://www.google.com/search?tbm=isch&q=Saul+Leiter+color+photography) |
| F01 | Miguel Ángel, *David* | **Alexander Calder**, *Lobster Trap and Fish Tail* (1939) | Ya está elegida (MoMA); sirve otro móvil si hay mejor imagen | [buscar](https://www.google.com/search?tbm=isch&q=Calder+Lobster+Trap+and+Fish+Tail) |
| F02 | Rodin, *El pensador* | **Gyula Kosice** | Una hidroescultura (agua y luz) | [buscar](https://www.google.com/search?tbm=isch&q=Gyula+Kosice+hidroescultura) |
| F05 | Bernini, *Apolo y Dafne* | **Ruth Asawa** | Una escultura colgante de alambre tejido | [buscar](https://www.google.com/search?tbm=isch&q=Ruth+Asawa+hanging+wire+sculpture) |
| G07 | Pollock, *Blue Poles* | **Sheila Hicks** | Una obra textil de pared | [buscar](https://www.google.com/search?tbm=isch&q=Sheila+Hicks+textile+work) |
| H05 | Duchamp, *L.H.O.O.Q.* | **Rogelio Polesello** | Una pintura op-art (años 60–70) | [buscar](https://www.google.com/search?tbm=isch&q=Rogelio+Polesello+pintura+op+art) |
| I03 | Yoko Ono, *Cut Piece* | **Lucio Fontana**, *Concetto spaziale, Attese* | Una tela con tajos (anotá el año de la que elijas) | [buscar](https://www.google.com/search?tbm=isch&q=Lucio+Fontana+Concetto+spaziale+Attese) |
| I04 | Hirst, el tiburón | **Liliana Porter** | Una obra con figuritas o juguetes chicos | [buscar](https://www.google.com/search?tbm=isch&q=Liliana+Porter+figurines+obra) |
| J02 | Kosuth (estaba duplicada con I02) | **Jorge Macchi** | Una obra sobre papel u objeto chico | [buscar](https://www.google.com/search?tbm=isch&q=Jorge+Macchi+obra) |
| J04 | Cindy Sherman, *Film Still #35* | **Carlos Cruz-Diez**, serie *Physichromie* | Una Physichromie de franjas de color | [buscar](https://www.google.com/search?tbm=isch&q=Carlos+Cruz-Diez+Physichromie) |
| J05 | Smithson, *Spiral Jetty* | **Julio Le Parc** | Una obra lumínica o móvil | [buscar](https://www.google.com/search?tbm=isch&q=Julio+Le+Parc+continuel+lumi%C3%A8re) |

**Ojo con J04:** en `assets/manual/` ya hay un `J04.jpg`, que es la foto de Cindy Sherman.
Borralo y guardá la de Cruz-Diez con el mismo nombre.

Para ver qué falta en cualquier momento: `python tools/aplicar_curaduria.py --listar`.
Los borradores de cada obra nueva (vector, familia y texto "mirá esto") están en
`data/curaduria_1_1.json`.

## Paso 2 · Doble evaluación de los vectores

Los 8 valores de cada obra los asignó una IA. La revisión recomienda que los asignen **dos
personas por separado** (vos y alguien del mundo del arte) para detectar desacuerdos. Conviene
hacerlo **después** del paso 1, así se evalúan las 60 obras finales.

1. Yo genero la planilla con `python tools/evaluacion_vectores.py plantilla`
   (queda en `docs/evaluacion/plantilla_vectores.csv`; ya hay una versión inicial).
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

Sobre **E7**: hoy ninguna obra tiene valor negativo (el promedio es +0,68), así que en la
práctica el eje no distingue nada. Al evaluar, usá toda la escala: una acuarela chica o una foto
íntima deberían ir claramente hacia -1.
