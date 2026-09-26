#!/usr/bin/env python3
"""Construye el catálogo de la curaduría 2.0 (docs/CURADURIA_2_0.md) desde cero.

- Archiva el catálogo anterior en data/archivo_v1/ (una sola vez).
- Escribe data/artworks.json e data/image_sources.json con las 60 obras nuevas.
- Copia/baja cada imagen a assets/manual/ID.jpg (luego se procesan con fetch_images.py).

Vectores (8 ejes, -1..1) = borrador de Claude hasta la doble evaluación.
Orden de los ejes: E1 Abstracto↔Figurativo, E2 Estructurado↔Espontáneo, E3 Sereno↔Expresivo,
E4 Contenido↔Saturado, E5 Plano↔Material, E6 Cotidiano↔Imaginario, E7 Íntimo↔Dominante,
E8 Transparente↔Conceptual.
"""
import json, shutil, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, MANUAL, OLD_IMG = ROOT / "data", ROOT / "assets" / "manual", ROOT / "assets" / "artworks"
ARCH = DATA / "archivo_v1"
AXES = ["E1 Abstracto↔Figurativo", "E2 Estructurado↔Espontáneo", "E3 Sereno↔Expresivo",
        "E4 Contenido↔Saturado", "E5 Plano↔Material", "E6 Cotidiano↔Imaginario",
        "E7 Íntimo↔Dominante", "E8 Transparente↔Conceptual"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
WA = "https://uploads{}.wikiart.org/"

F = {"GE": "Geometric abstraction", "CI": "Kinetic / optical art", "CF": "Color field / atmospheric abstraction",
     "GS": "Gestural abstraction", "MA": "Material: textile, ceramic & sculpture", "FI": "Figuration",
     "FO": "Photography", "PA": "Landscape", "IM": "Imaginary / surreal", "CO": "Idea, object & pop"}

# (ID, Título, Artista, Año, Medio, origen A/I, fama 1-3, imagen, fuente, vector, contexto)
# imagen: "old:ID" = imagen del catálogo anterior; URL = se baja.
W = [
 ("GE01", "4 temas circulares", "Tomás Maldonado", 1953, "Oil on canvas", "A", 1,
  "https://uploads1.wikiart.org/images/tomas-maldonado/4-temas-circulares-1953.jpg", "WikiArt",
  [-1, -0.9, -0.2, 0.1, -0.6, 0, 0.2, 0.3],
  "Maldonado fue uno de los fundadores del arte concreto en Buenos Aires: nada representa nada, todo es forma y color. Mirá cómo cuatro círculos alcanzan para armar un ritmo, y cómo el fondo trabaja tanto como las figuras."),
 ("GE02", "Pintura perceptista nº 184", "Raúl Lozza", 1948, "Enamel on wood", "A", 1,
  "https://uploads3.wikiart.org/images/raul-lozza/pintura-perceptista-n-184-1948.jpg", "WikiArt",
  [-1, -0.9, -0.3, -0.2, -0.5, 0, 0, 0.3],
  "Lozza inventó el 'perceptismo': formas planas de color puestas directamente sobre la pared o un fondo liso. Mirá cómo cada forma parece flotar y cómo cambia la sensación según qué color tengas al lado."),
 ("GE03", "1510", "Pablo Siquier", 2015, "Acrylic on canvas", "A", 1,
  "https://ruthbenzacar.com/wp-content/uploads/2017/02/1510-150-x-260-cm.jpg", "Ruth Benzacar",
  [-0.9, -1, 0.1, -0.3, -0.8, 0.2, 0.6, 0.4],
  "Siquier dibuja como un arquitecto que se volvió loco de precisión: líneas negras que arman volúmenes imposibles. Mirá cómo la imagen parece una fachada o un plano, pero no lleva a ningún lugar real."),
 ("GE04", "Vibración al infinito", "Lidy Prati", 1953, "Oil on canvas", "A", 1,
  "https://uploads8.wikiart.org/images/lidy-prati/vibraci-n-al-infinito-1953.jpg", "WikiArt",
  [-1, -0.9, 0.2, 0, -0.6, 0.1, 0.3, 0.3],
  "Lidy Prati fue una de las pioneras del arte concreto argentino. Mirá cómo formas mínimas, repetidas y ordenadas, generan una vibración que parece seguir más allá de los bordes del cuadro."),
 ("GE05", "Composition II in Red, Blue, and Yellow", "Piet Mondrian", 1930, "Oil on canvas", "I", 3,
  "old:A02", "Wikimedia Commons",
  [-1, -0.9, -0.3, -0.4, -0.6, -0.1, 0.1, 0.1], None),
 ("GE06", "Homage to the Square: Apparition", "Josef Albers", 1959, "Oil on masonite", "I", 2,
  "https://uploads2.wikiart.org/00305/images/josef-albers/homage-to-the-square-apparition.jpg", "WikiArt",
  [-1, -1, -0.6, -0.3, -0.6, 0, -0.1, 0.3],
  "Albers pintó cientos de cuadrados dentro de cuadrados para estudiar una sola cosa: cómo un color cambia según el que tiene al lado. Mirá los bordes: ahí es donde el color 'vibra'."),
 ("GE07", "Red Blue Green", "Ellsworth Kelly", 1963, "Oil on canvas", "I", 2,
  "https://uploads6.wikiart.org/images/ellsworth-kelly/red-blue-green-1963.jpg", "WikiArt",
  [-1, -0.8, 0, 0.3, -0.9, 0, 0.6, 0.2],
  "Kelly reduce todo a tres colores y dos formas. Mirá la tensión entre la curva y el bloque recto, y cómo el color plano, sin pinceladas, hace que la forma se sienta casi como un objeto."),
 ("GE08", "The Ten Largest, No. 7, Adulthood", "Hilma af Klint", 1907, "Tempera on paper mounted on canvas", "I", 2,
  "old:A04", "Wikimedia Commons (dominio público)",
  [-0.8, 0.1, 0.3, 0.6, -0.3, 0.7, 0.7, 0.4], None),

 ("CI01", "Sin título", "Rogelio Polesello", 1959, "Paint on paper", "A", 1, "old:H05", "MALBA",
  [-1, -0.9, 0.3, 0.5, -0.7, 0.1, 0.5, 0.2], None),
 ("CI02", "Continuel Mobile Lumière", "Julio Le Parc", 1968, "Mixed media / light and movement", "A", 2, "old:J05", "WikiArt",
  [-1, -0.5, 0.4, 0.3, 0.4, 0.5, 0.8, 0.4], None),
 ("CI03", "Atmosphère chromoplastique N° 187", "Luis Tomasello", 1968, "Painted wood relief", "A", 1,
  "https://uploads5.wikiart.org/images/luis-tomasello/atmosph-re-chromoplastique-n-187-1968.jpg", "WikiArt",
  [-1, -0.9, -0.4, -0.6, 0.5, 0.1, 0.2, 0.3],
  "Tomasello pinta de color sólo la cara oculta de pequeños cubos blancos: lo que ves es el reflejo. Mirá cómo aparece un color suave en la superficie que nadie pintó."),
 ("CI04", "Physichromie No. 326", "Carlos Cruz-Diez", 1967, "Mixed media relief", "I", 2, "old:J04", "WikiArt",
  [-1, -0.9, 0, 0.2, 0.3, 0.1, 0.5, 0.3], None),
 ("CI05", "Movement in Squares", "Bridget Riley", 1961, "Tempera on board", "I", 2,
  "https://uploads0.wikiart.org/images/bridget-riley/movement-in-squares-1961.jpg", "WikiArt",
  [-1, -0.9, 0.5, -0.3, -0.8, 0.1, 0.6, 0.2],
  "Riley usa sólo blanco y negro: cuadrados que se van achicando hacia el centro. Mirá el pliegue que aparece en el medio; el cuadro es plano, pero tu ojo lo curva."),

 ("CF01", "Halo veronés", "Silvia Gurfein", 2024, "Oil on canvas", "A", 1,
  "https://norafisch.com/wp-content/uploads/2018/01/Silvia-Gurfein-Halo-verones-Nuevas-conversaciones-en-la-era-de-plomo-Oil-on-canvas-74-x-52-cm-2024.jpg", "Nora Fisch",
  [-0.6, 0.2, -0.5, 0, -0.3, 0.5, -0.4, 0.3],
  "Gurfein pinta luces y halos que parecen flotar en un espacio sin arriba ni abajo. Mirá cómo el color se funde de a poco y cómo el formato chico invita a acercarse."),
 ("CF02", "No. 61 (Rust and Blue)", "Mark Rothko", 1953, "Oil on canvas", "I", 3,
  "https://uploads3.wikiart.org/00158/images/mark-rothko/1.jpg", "WikiArt",
  [-0.9, -0.2, -0.3, 0.4, -0.2, 0.2, 0.8, 0.2],
  "Rothko quería que te pararas cerca, hasta que el color te envolviera. Mirá los bordes borrosos de cada bloque: no están recortados, respiran."),
 ("CF03", "Mountains and Sea", "Helen Frankenthaler", 1952, "Oil and charcoal on canvas", "I", 2,
  "https://uploads4.wikiart.org/images/helen-frankenthaler/mountains-and-sea-1962.jpg", "WikiArt",
  [-0.7, 0.6, -0.2, 0.2, -0.6, 0.3, 0.6, 0],
  "Frankenthaler volcaba pintura muy diluida sobre la tela cruda, que la absorbía como una acuarela gigante. Mirá lo liviano del color y cómo sugiere un paisaje sin dibujarlo."),
 ("CF04", "Night Sea", "Agnes Martin", 1963, "Oil and gold leaf on canvas", "I", 2,
  "https://uploads7.wikiart.org/images/agnes-martin/night-sea-1963.jpg", "WikiArt",
  [-1, -0.8, -1, -0.7, -0.4, 0, -0.2, 0.4],
  "Agnes Martin trazaba grillas a mano, con paciencia infinita. Mirá cómo la línea tiembla apenas: es lo que hace que una cuadrícula se sienta tranquila y no mecánica."),

 ("GS01", "The Hard Way", "Sarah Grilo", 1968, "Oil on canvas", "A", 1,
  "https://www.jorgemaralaruche.com.ar/sitiodos/wp-content/uploads/2014/08/2-Sarah-Grilo-The-Hard-Way-Oil-on-Canvas-114x114-cm-1968.jpg", "Jorge Mara – La Ruche",
  [-0.6, 0.8, 0.4, 0.2, 0.3, 0.2, 0.3, 0.4],
  "Grilo mezcla manchas de color con números, letras y palabras garabateadas, como una pared de la ciudad. Mirá cómo el texto se vuelve parte de la pintura y deja de leerse."),
 ("GS02", "Sin título", "Joaquín Boz", 2024, "Oil on canvas", "A", 1,
  "https://barro.cc/images/Image/2541/original/BA_BOZ-2.jpg", "Barro",
  [-0.9, 0.8, 0.6, 0.8, 0.4, 0.2, 0.8, 0],
  "Boz trabaja por capas, tapando y dejando ver. Mirá cuántos colores conviven sin ordenarse y cómo el ojo nunca termina de recorrer el cuadro."),
 ("GS03", "Gracias", "Fernanda Laguna", 2025, "Acrylic and glitter on canvas with cut-outs", "A", 1,
  "https://norafisch.com/wp-content/uploads/2017/10/Fernanda-Laguna_Gracias_Acrylic-and-glitter-on-canvas-with-cut-outs_104-x-80n-cm_2025.jpg", "Nora Fisch",
  [-0.4, 0.6, 0.5, 0.6, 0.4, 0.6, 0, 0.2],
  "Laguna pinta con brillantina, recortes y formas que parecen hechas sin pensar. Mirá cómo lo 'desprolijo' es una decisión: la obra se siente cercana, casi como un regalo hecho a mano."),
 ("GS04", "Ladybug", "Joan Mitchell", 1957, "Oil on canvas", "I", 2,
  "https://uploads6.wikiart.org/images/joan-mitchell/ladybug-1957.jpg", "WikiArt",
  [-0.9, 1, 0.8, 0.6, 0.6, 0.1, 0.7, -0.1],
  "Mitchell pintaba con todo el brazo, a gran velocidad. Mirá la energía de cada trazo y cómo, entre tanto movimiento, el blanco del fondo deja respirar al cuadro."),
 ("GS05", "Abstract Painting 780-1", "Gerhard Richter", 1992, "Oil on canvas", "I", 2,
  "https://uploads1.wikiart.org/images/gerhard-richter/abstract-painting-780-1.jpg", "WikiArt",
  [-1, 0.6, 0.5, 0.6, 0.8, 0.1, 0.7, 0.2],
  "Richter arrastra capas de pintura con una espátula enorme: lo que aparece es en parte control y en parte azar. Mirá las raspaduras que dejan ver los colores de abajo."),
 ("GS06", "Leda and the Swan", "Cy Twombly", 1962, "Oil, pencil and crayon on canvas", "I", 2,
  "https://uploads8.wikiart.org/images/cy-twombly/leda-and-the-swan.jpg", "WikiArt",
  [-0.6, 1, 0.9, 0.3, 0.4, 0.4, 0.6, 0.5],
  "Twombly pinta un mito griego como si fuera un garabato furioso. Mirá cómo, entre las marcas, aparecen formas que casi se reconocen y enseguida se pierden."),
 ("GS07", "Composition VII", "Wassily Kandinsky", 1913, "Oil on canvas", "I", 3, "old:B02", "Wikimedia Commons",
  [-0.9, 0.2, 0.9, 0.8, 0.2, 0.2, 0.8, 0.2], None),

 ("MA01", "Concetto spaziale, Attesa", "Lucio Fontana", 1966, "Water-based paint on canvas, slashed", "A", 2, "old:I03", "WikiArt",
  [-1, -0.2, 0.3, -0.8, 0.6, 0.2, 0.5, 0.8], None),
 ("MA02", "Deformación de la gota circunvalada", "Gyula Kosice", 1965, "Acrylic and water", "A", 1, "old:F02", "WikiArt",
  [-0.6, -0.5, -0.4, -0.6, 0.5, 0.5, 0.3, 0.4], None),
 ("MA03", "Criollos en la piscina", "Chiachio & Giannone", 2019, "Textile mosaic", "A", 1,
  "https://ruthbenzacar.com/wp-content/uploads/2016/11/chiachiogiannone_criollos-en-la-piscina2018_baja.jpg", "Ruth Benzacar",
  [0.6, 0.3, 0.3, 0.8, 0.9, 0.5, 0.6, 0.3],
  "Chiachio & Giannone bordan a mano escenas llenas de humor, con telas recicladas como si fueran pintura. Mirá cuánto tiempo de trabajo hay en cada pedacito, y la escena de pileta que guiña a la pintura de Hockney."),
 ("MA04", "Sin título", "Marina De Caro", 2015, "Glazed ceramics with interventions", "A", 1,
  "https://ruthbenzacar.com/wp-content/uploads/2017/02/0000016335_S_.jpg", "Ruth Benzacar",
  [-0.3, 0.5, 0.2, 0.5, 1, 0.4, 0.1, 0.3],
  "De Caro trabaja la cerámica como si fuera dibujo: formas blandas, esmaltes de color, piezas que parecen crecer. Mirá la superficie brillante y las marcas de la mano en el barro."),
 ("MA05", "Inawop [La primavera]", "Claudia Alarcón & Silät", 2023, "Hand-woven chaguar fiber", "A", 1,
  "https://static-assets.artlogic.net/w_1600,h_1600,c_limit,f_auto,fl_lossy,q_auto/artlogicstorage/cbprojects/images/view/e7c76c0e22a2b8c1c9d639aae8a8b875j.jpg", "Cecilia Brunson Projects",
  [-0.6, -0.4, -0.2, 0.2, 0.9, 0.4, 0.3, 0.2],
  "Tejedoras wichí de Salta, con una técnica ancestral en fibra de chaguar, arman composiciones abstractas nuevas. Mirá cómo el diseño se construye punto por punto, y la textura que sólo tiene lo hecho a mano."),
 ("MA06", "Estoy viva", "Josefina Labourt", 2024, "Fabric, resin, paper, wood, acrylic and oil", "A", 1,
  "https://piedrasgaleria.com/wp-content/uploads/2022/03/DSC8050.jpg", "Piedras",
  [0.1, 0.6, 0.5, -0.2, 1, 0.4, -0.2, 0.5],
  "Labourt arma relieves con tela, resina y papel que parecen piel o algo vivo. Mirá cómo la forma se sale del plano y cómo la palabra modelada en la superficie se vuelve materia."),
 ("MA07", "Grand Prayer Rug", "Sheila Hicks", 1966, "Textile / fiber", "I", 2, "old:G07", "WikiArt",
  [-0.8, 0.3, 0, -0.2, 1, 0.1, 0.5, 0.1], None),
 ("MA08", "Untitled (S.270)", "Ruth Asawa", 1955, "Looped wire", "I", 2, "old:F05", "Whitney Museum of American Art",
  [-0.7, -0.3, -0.5, -0.3, 0.8, 0.2, 0.4, 0.1], None),
 ("MA09", "Lobster Trap and Fish Tail", "Alexander Calder", 1939, "Painted steel wire and sheet aluminum", "I", 2, "old:F01", "WikiArt (MoMA)",
  [-0.7, 0.2, 0.1, 0.1, 0.5, 0.3, 0.6, 0.1], None),
 ("MA10", "Intersecting", "Anni Albers", 1962, "Woven cotton and rayon", "I", 1,
  "https://uploads0.wikiart.org/images/anni-albers/intersecting-1962.jpg", "WikiArt",
  [-1, -0.8, -0.3, -0.2, 0.7, 0, -0.3, 0.2],
  "Anni Albers llevó la geometría moderna al telar. Mirá cómo las líneas se cruzan y se esconden entre los hilos: es un cuadro abstracto, pero hecho tejiendo."),
 ("MA11", "Bird in Space", "Constantin Brâncuși", 1928, "Bronze", "I", 2, "old:F03", "Wikimedia Commons",
  [-0.6, -0.8, -0.2, -0.6, 0.7, 0.4, 0.4, 0.2], None),

 ("FI01", "Manifestación", "Antonio Berni", 1934, "Tempera on burlap", "A", 2, "old:C04", "WikiArt",
  [0.9, -0.2, 0.5, 0.3, 0.2, -0.5, 0.8, 0.3], None),
 ("FI02", "Lamp Light Knitt", "Alejandra Seeber", 2025, "Oil on canvas", "A", 1,
  "https://ruthbenzacar.com/wp-content/uploads/2026/04/Captura-de-Pantalla-2026-04-09-a-las-13.25.44.png", "Ruth Benzacar",
  [0.4, 0.3, 0, 0.6, 0.5, 0.2, -0.2, 0.2],
  "Seeber pinta objetos de la casa (una lámpara, una mesa) sobre un fondo que imita un tejido a mano. Mirá cómo lo doméstico se vuelve patrón y color, entre la pintura y la decoración."),
 ("FI03", "Fuego", "Carrie Bencardino", 2022, "Oil on canvas", "A", 1,
  "https://piedrasgaleria.com/wp-content/uploads/2022/06/CarrieBencardino_FeriaMaterial3.jpg", "Piedras",
  [0.9, 0.6, 0.8, 0.5, 0.3, 0.2, 0.6, 0.1],
  "Bencardino pinta escenas de noche, de amigos y de calle, con caras muy cerca. Mirá la luz del encendedor y cómo el encuadre apretado te mete dentro de la escena."),
 ("FI04", "Primavera", "Constanza Giuliani", 2024, "Acrylic on canvas, airbrush", "A", 1,
  "https://piedrasgaleria.com/wp-content/uploads/2022/03/H3A0763.jpg", "Piedras",
  [0.6, 0.3, 0.4, 0.7, -0.5, 0.8, 0.2, 0.3],
  "Giuliani pinta con aerógrafo, como en el grafiti o la historieta, personajes entre tiernos y raros. Mirá cómo la criatura se mezcla con las flores y cómo el color parece de dibujo animado."),
 ("FI05", "A Bigger Splash", "David Hockney", 1967, "Acrylic on canvas", "I", 3, "old:C05", "Wikipedia",
  [0.5, -0.5, -0.2, 0.2, -0.8, -0.3, 0.5, 0.2], None),
 ("FI06", "Morning Sun", "Edward Hopper", 1952, "Oil on canvas", "I", 3,
  "https://uploads5.wikiart.org/images/edward-hopper/morning-sun.jpg", "WikiArt",
  [0.9, -0.4, -0.4, -0.4, -0.4, -0.6, 0.3, 0.1],
  "Hopper pinta a una mujer sola mirando por la ventana con la primera luz del día. Mirá cómo el sol dibuja rectángulos en la pared y cómo la escena es tranquila y un poco melancólica a la vez."),
 ("FI07", "The Red Smile", "Alex Katz", 1963, "Oil on canvas", "I", 2,
  "https://uploads3.wikiart.org/images/alex-katz/the-red-smile.jpg", "WikiArt",
  [0.8, -0.5, 0, 0.3, -0.9, -0.3, 0.7, 0],
  "Katz pinta retratos como carteles: colores planos, fondo liso, sin sombras. Mirá cómo el rojo del fondo hace que un gesto simple, una sonrisa, se vuelva enorme."),

 ("FO01", "Corrientes", "Horacio Coppola", 1936, "Gelatin silver print", "A", 1,
  "https://www.jorgemaralaruche.com.ar/sitiodos/wp-content/uploads/2014/08/Horacio-Coppola-Corrientes-1936.jpg", "Jorge Mara – La Ruche",
  [0.7, -0.5, -0.1, -0.3, -0.4, -0.5, 0.5, 0],
  "Coppola fotografió la Buenos Aires moderna de los años 30, recién construida. Mirá la calle Corrientes de noche, convertida en un río de luz entre edificios."),
 ("FO02", "Eugenia y Violeta, de la serie Madres e hijas", "Adriana Lestido", 1995, "Gelatin silver print", "A", 1,
  "https://rolfart.com.ar/wp-content/uploads/2024/11/Adriana-Lestido-Madres-e-hijas-Eugenia-y-Violeta-1995-1998-gelatina-de-plata-sobre-papel-fibra-dimensiones-variables-15AP-5.jpg", "Rolf Art",
  [0.8, 0.4, 0.5, -0.6, -0.2, -0.8, -0.6, 0],
  "Lestido pasó años fotografiando a madres e hijas en su vida diaria. Mirá el movimiento borroso de la nena: la foto no posa, captura un instante que se escapa."),
 ("FO03", "Bruma I – Ministerio I", "Santiago Porter", 2007, "Archival pigment print", "A", 1,
  "https://rolfart.com.ar/wp-content/uploads/2025/10/Santiago-Porter-Bruma-I-Ministerio-I-2007-fotografia-impresion-con-tintas-perdurables-sobre-papel-fotografico-127-x-1586-cm-edicion-5-2AP.jpg", "Rolf Art",
  [0.7, -0.8, -0.6, -0.7, -0.2, -0.4, 0.4, 0.4],
  "Porter fotografía edificios públicos de frente, quietos y simétricos. Mirá cómo, sin personas, la arquitectura sola habla del poder y del paso del tiempo."),
 ("FO04", "Red Umbrella", "Saul Leiter", 1958, "Chromogenic print", "I", 2, "old:E07", "artblart.com",
  [0.3, 0.3, -0.2, 0.1, 0, -0.4, -0.4, 0], None),
 ("FO05", "Seascape: Aegean Sea, Pillon", "Hiroshi Sugimoto", 1990, "Gelatin silver print", "I", 2, "old:D03", "WikiArt",
  [-0.4, -0.8, -0.9, -0.9, -0.4, 0.2, 0.3, 0.4], None),
 ("FO06", "The Red Ceiling (Greenwood, Mississippi)", "William Eggleston", 1973, "Dye transfer print", "I", 2,
  "https://uploads4.wikiart.org/images/william-eggleston/the-red-ceiling-greenwood-mississippi-1973.jpg", "WikiArt",
  [0.6, -0.2, 0.3, 0.8, -0.4, -0.6, 0.2, 0.1],
  "Eggleston fue de los primeros en tomarse en serio la foto color de lo cotidiano. Mirá cómo un techo rojo y una lamparita alcanzan para que un cuarto común se vuelva intenso."),

 ("PA01", "Trayecto", "Matías Duville", 2010, "Charcoal and pastel on paper", "A", 1,
  "https://barro.cc/images/Image/2666/original/BA_DUVILLE-8.jpg", "Barro",
  [0.3, 0.4, 0.4, -0.5, 0.4, 0.3, 0.6, 0.1],
  "Duville dibuja paisajes enormes con carbonilla, entre mapa y sueño. Mirá los ríos que atraviesan la roca: se reconoce un territorio, pero no existe en ningún lado."),
 ("PA02", "Mount Tamalpais", "Etel Adnan", 1985, "Painting", "I", 1, "old:D04", "WikiArt (Sursock Museum)",
  [-0.3, -0.2, -0.3, 0.4, 0.2, 0.1, -0.4, 0], None),
 ("PA03", "White Canoe", "Peter Doig", 1991, "Oil on canvas", "I", 2,
  "https://uploads7.wikiart.org/images/peter-doig/white-canoe-1991.jpg", "WikiArt",
  [0.5, 0.3, -0.3, 0.4, 0.1, 0.6, 0.4, 0.1],
  "Doig pinta paisajes como si fueran un recuerdo o un sueño. Mirá la canoa blanca y su reflejo: todo es reconocible, pero los colores y la quietud lo vuelven irreal."),

 ("IM01", "Drago", "Xul Solar", 1927, "Watercolor on paper", "A", 2, "old:B06", "WikiArt",
  [0.2, 0.1, 0.4, 0.7, -0.5, 0.9, -0.2, 0.5], None),
 ("IM02", "Sueño Nº 1: Artículos eléctricos para el hogar", "Grete Stern", 1950, "Photomontage, gelatin silver print", "A", 1,
  "https://www.jorgemaralaruche.com.ar/sitiodos/wp-content/uploads/2014/08/Grete-Stern-Sueno-Nro1-Articulos-electricos-para-el-hogar-1950.jpg", "Jorge Mara – La Ruche",
  [0.8, -0.2, 0.3, -0.5, -0.4, 0.8, 0, 0.7],
  "Grete Stern ilustraba los sueños que las lectoras de una revista mandaban para interpretar. Mirá cómo, con un fotomontaje, una mujer se vuelve una lámpara: humor, surrealismo y crítica, todo junto."),
 ("IM03", "Inundación con árbol, nido y cuadro", "Marcelo Pombo", 2006, "Enamel on panel", "A", 1,
  "https://barro.cc/images/Image/111/original/ba-pombo-inundacion.jpg", "Barro",
  [0.6, -0.1, -0.2, 0.2, -0.2, 0.8, 0.2, 0.4],
  "Pombo pinta con esmalte, con una paciencia de miniaturista, escenas que parecen de cuento. Mirá el cuadro dentro del cuadro, colgado del árbol: una imagen tranquila y absurda a la vez."),
 ("IM04", "The Empire of Light", "René Magritte", 1954, "Oil on canvas", "I", 3,
  "https://uploads4.wikiart.org/images/rene-magritte/the-empire-of-lights-1954(1).jpg", "WikiArt",
  [0.8, -0.5, -0.6, -0.3, -0.4, 0.8, 0.4, 0.6],
  "Magritte pinta una calle de noche bajo un cielo de pleno día. Tardás un segundo en notarlo. Mirá cómo algo imposible puede sentirse completamente sereno."),
 ("IM05", "Creation of the Birds", "Remedios Varo", 1957, "Oil on masonite", "I", 2,
  "https://uploads6.wikiart.org/images/remedios-varo/creation-of-the-birds.jpg", "WikiArt",
  [0.8, -0.2, 0.2, 0.2, -0.2, 1, 0.1, 0.5],
  "Varo, surrealista que vivió en México, pinta una mujer-búho que crea pájaros con luz de estrella y un prisma. Mirá el detalle de cada objeto: es un mundo inventado con reglas propias."),

 ("CO01", "Buenos Aires Tour", "Jorge Macchi", 2003, "Book and installation (mixed media)", "A", 1, "old:J02", "jorgemacchi.com",
  [0.2, 0, -0.1, 0.1, 0.1, 0.2, 0.1, 0.9], None),
 ("CO02", "Diálogo (con pingüino)", "Liliana Porter", 1998, "Cibachrome on polyester", "A", 1, "old:I04", "Museo Reina Sofía",
  [0.7, -0.3, 0.1, -0.6, -0.2, 0.6, -0.6, 0.8], None),
 ("CO03", "Campbell's Soup Cans", "Andy Warhol", 1962, "Synthetic polymer paint on canvas", "I", 3, "old:H04", "Wikimedia Commons",
  [0.6, -0.8, 0.1, 0.8, -0.8, 0.2, 0.8, 0.5], None),
 ("CO04", "Pumpkin", "Yayoi Kusama", 1990, "Acrylic on canvas", "I", 3,
  "https://uploads5.wikiart.org/images/yayoi-kusama/pumpkin-1990.jpg", "WikiArt",
  [0.3, -0.5, 0.4, 0.7, -0.3, 0.5, 0.4, 0.4],
  "Kusama cubre todo de puntos, una obsesión que la acompaña desde chica. Mirá cómo la calabaza, un objeto cualquiera, se vuelve un patrón que casi vibra."),
]


def main():
    old = json.loads((DATA / "artworks.json").read_text(encoding="utf-8"))
    old_by = {w["ID"]: w for w in old}
    if not ARCH.exists():
        ARCH.mkdir()
        for f in ("artworks.json", "duels.json", "image_sources.json", "image_manifest.json", "curaduria_1_1.json"):
            if (DATA / f).exists():
                shutil.copyfile(DATA / f, ARCH / f)
        print("Catálogo anterior archivado en data/archivo_v1/")
    assert len(W) == 60 and len({w[0] for w in W}) == 60

    out, sources = [], {"_README": "Curaduría 2.0: todas las imágenes vienen de assets/manual/ID.jpg (ver tools/curaduria_2_0.py para la fuente de cada una)."}
    for (code, title, artist, year, medium, origin, fame, img, src, vec, ctx) in W:
        if img.startswith("old:"):
            o = old_by[img[4:]]
            ctx = ctx or o.get("context", "")
            shutil.copyfile(OLD_IMG / f"{img[4:]}.jpg", MANUAL / f"{code}.jpg")
        elif not (MANUAL / f"{code}.jpg").exists():
            for intento in range(3):
                try:
                    data = urllib.request.urlopen(urllib.request.Request(img, headers={**UA, "Referer": img}), timeout=120).read()
                    break
                except Exception as e:
                    print(f"  {code}: reintento ({e})")
            else:
                raise SystemExit(f"{code}: no se pudo bajar {img}")
            (MANUAL / f"{code}.jpg").write_bytes(data)
            print(f"  {code}: bajada ({len(data) // 1024} KB)")
        w = {"ID": code, "Título": title, "Artista": artist, "Año": year, "Medio": medium,
             "Familia": F[code[:2]], "Origen": "Argentina" if origin == "A" else "Internacional",
             "Fama": fame, "Fuente/licencia": f"Imagen: {src} (uso educativo, prueba privada)"}
        w.update(dict(zip(AXES, vec)))
        w.update({"image_source": src, "image_status": "MANUAL", "image_url": "", "context": ctx,
                  "image_file": f"assets/artworks/{code}.jpg"})
        out.append(w)
        sources[code] = {"wiki": [], "fuente": src, "url_original": "" if img.startswith("old:") else img}
    (DATA / "artworks.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    (DATA / "image_sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"{len(out)} obras escritas. Ahora: python tools/fetch_images.py --force")


if __name__ == "__main__":
    sys.exit(main())
