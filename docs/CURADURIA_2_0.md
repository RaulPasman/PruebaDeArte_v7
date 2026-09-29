# Curaduría 2.0 — aplicada

Aplicada el 26/09/2026. Basada en `docs/RELEVAMIENTO_TENDENCIAS_2026.md` y en las definiciones de
Raúl:

- **Objetivo:** medir el gusto de cada persona con la mayor precisión posible. Lo comercial
  (vincular con galerías de CABA) viene después, en unos 6 meses.
- **~60% abstracción** (39 obras, contando la familia de minimalismo cálido) y el resto otros lenguajes.
- **Mitad argentinas, mitad referencias internacionales** (30 y 30). Todas las argentinas tienen
  galería en Capital, así quedan listas para la etapa comercial.

El catálogo anterior (v1) quedó archivado en `data/archivo_v1/` y sus imágenes manuales en
`assets/manual/archivo_v1/`. Todo se reconstruye con `python tools/curaduria_2_0.py` (datos y
fuentes de cada imagen) y `python tools/armar_duelos.py` (duelos).

## Criterios

1. **Cada obra está para distinguir gustos**: es un ejemplo claro de una forma de mirar (orden,
   gesto, materia, color, figura, idea), no un ícono que se elige "porque lo conozco".
2. **Referencias internacionales vigentes** (Albers, Rothko, Joan Mitchell, Richter, Hockney,
   Kusama, textil) en vez de maestros antiguos; se sacaron los súper íconos.
3. **Obras "de casa"**: colgables o de apoyo.
4. **Duelos justos**: nunca dos obras de la misma familia, y fama parecida entre las dos (campo
   `Fama`, 1 a 3), para que no gane la conocida. Varios duelos enfrentan dos abstracciones de
   distinto tipo, porque al público mayormente abstracto hay que distinguirle *qué* abstracción
   prefiere.

## Las 60 obras

A = argentina · I = internacional. Fuente de cada imagen en `tools/curaduria_2_0.py`.

| ID | Obra | Artista | Año | Origen |
|---|---|---|---|---|
| GE01 | 4 temas circulares | Tomás Maldonado | 1953 | A |
| GE03 | 1510 | Pablo Siquier | 2015 | A |
| GE04 | Vibración al infinito | Lidy Prati | 1953 | A |
| GE05 | Composition II in Red, Blue, and Yellow | Piet Mondrian | 1930 | I |
| GE06 | Homage to the Square: Apparition | Josef Albers | 1959 | I |
| GE07 | Red Blue Green | Ellsworth Kelly | 1963 | I |
| GE08 | The Ten Largest, No. 7, Adulthood | Hilma af Klint | 1907 | I |
| CI01 | Sin título | Rogelio Polesello | 1959 | A |
| CI02 | Continuel Mobile Lumière | Julio Le Parc | 1968 | A |
| CI03 | Atmosphère chromoplastique N° 187 | Luis Tomasello | 1968 | A |
| CI04 | Physichromie No. 326 | Carlos Cruz-Diez | 1967 | I |
| CI05 | Movement in Squares | Bridget Riley | 1961 | I |
| CF01 | Halo veronés | Silvia Gurfein | 2024 | A |
| CF03 | Mountains and Sea | Helen Frankenthaler | 1952 | I |
| CF04 | Night Sea | Agnes Martin | 1963 | I |
| GS01 | The Hard Way | Sarah Grilo | 1968 | A |
| GS02 | Sin título | Joaquín Boz | 2024 | A |
| GS03 | Gracias | Fernanda Laguna | 2025 | A |
| GS04 | Ladybug | Joan Mitchell | 1957 | I |
| GS05 | Abstract Painting 780-1 | Gerhard Richter | 1992 | I |
| MA01 | Concetto spaziale, Attesa | Lucio Fontana | 1966 | A |
| MA02 | Deformación de la gota circunvalada | Gyula Kosice | 1965 | A |
| MA03 | Criollos en la piscina | Chiachio & Giannone | 2019 | A |
| MA05 | Inawop [La primavera] | Claudia Alarcón & Silät | 2023 | A |
| MA07 | Grand Prayer Rug | Sheila Hicks | 1966 | I |
| MA08 | Untitled (S.270) | Ruth Asawa | 1955 | I |
| MA09 | Lobster Trap and Fish Tail | Alexander Calder | 1939 | I |
| MA10 | Intersecting | Anni Albers | 1962 | I |
| FI02 | Lamp Light Knitt | Alejandra Seeber | 2025 | A |
| FI03 | Fuego | Carrie Bencardino | 2022 | A |
| FI05 | A Bigger Splash | David Hockney | 1967 | I |
| FI06 | Morning Sun | Edward Hopper | 1952 | I |
| FO01 | Corrientes | Horacio Coppola | 1936 | A |
| FO02 | Eugenia y Violeta, de la serie Madres e hijas | Adriana Lestido | 1995 | A |
| FO03 | Bruma I – Ministerio I | Santiago Porter | 2007 | A |
| FO04 | Red Umbrella | Saul Leiter | 1958 | I |
| FO05 | Seascape: Aegean Sea, Pillon | Hiroshi Sugimoto | 1990 | I |
| PA01 | Trayecto | Matías Duville | 2010 | A |
| PA02 | Mount Tamalpais | Etel Adnan | 1985 | I |
| PA03 | White Canoe | Peter Doig | 1991 | I |
| IM01 | Drago | Xul Solar | 1927 | A |
| IM02 | Sueño Nº 1: Artículos eléctricos para el hogar | Grete Stern | 1950 | A |
| IM03 | Inundación con árbol, nido y cuadro | Marcelo Pombo | 2006 | A |
| IM04 | The Empire of Light | René Magritte | 1954 | I |
| IM05 | Creation of the Birds | Remedios Varo | 1957 | I |
| CO01 | Buenos Aires Tour | Jorge Macchi | 2003 | A |
| CO02 | Diálogo (con pingüino) | Liliana Porter | 1998 | A |
| CO04 | Pumpkin | Yayoi Kusama | 1990 | I |
| MC02 | Wall of Light Desert Night | Sean Scully | 1999 | I |
| MC03 | Stairway | Alexander Rodchenko | 1930 | I |
| MC04 | Seascape (Cloudy) | Gerhard Richter | 1969 | I |
| MC05 | Pelagos | Barbara Hepworth | 1946 | I |
| MC06 | Geo impacto I, II, III | Marcela Cabutti | 2021 | A |
| MC07 | Sin título | Martín Reyna | 2021 | A |
| MC08 | Círculos XVII | Carola Zech | 2018 | A |
| FO06 | Roque Sáenz Peña | Horacio Coppola | 1936 | A |
| FO07 | Buenos Aires | Humberto Rivas | 1984 | A |
| CF05 | White Ground–Red Halo | Adolph Gottlieb | 1966 | I |
| CF06 | Untitled (Red) | Mark Rothko | 1956 | I |
| MC09 | Untitled | Lee Ufan | 2008 | I |

Cambios respecto de la propuesta, por disponibilidad de imágenes verificables: Marcolina
Dipierro → Lidy Prati; Karina Peisajovich → Luis Tomasello; Gimena Macri y Laura Ojeda Bär →
Fernanda Laguna y Constanza Giuliani; Erica Bohm → Santiago Porter; Clara Esborraz → Carrie
Bencardino (que resultó figurativa). La cerámica la cubre Marina De Caro.

## Motor recalibrado

Los vectores de los 9 perfiles se recalibraron para el catálogo nuevo (los viejos quedaron en
`data/archivo_v1/profiles.json`): varios perfiles estaban casi superpuestos (el imaginador se
confundía con el cazador de lo inesperado el 93% de las veces). Resultado del simulador:

| Medida | Antes (catálogo v1) | Ahora |
|---|---|---|
| Perfil principal correcto | ~59% | **~79%** |
| Principal o matiz | ~88% | **~92%** |
| Máximo de usuarios al azar en un mismo perfil | ~16% | ~17% |
| Persona "abstracción serena" (como Raúl) | salía "equilibrador" | **arquitecto 84% / atmósferas 16%** |
| Persona "abstracto de todo tipo" | equilibrador 90% | arquitecto 54% / equilibrador 43% |

Ajuste del 26/09/2026 (después de la primera prueba real de Raúl): "equilibrador" (P03) había
quedado como "abstracto a secas" y se llevaba a casi todo el que elige abstracción variada. Se
redefinió como "obras que combinan orden y gesto".

Confusiones que quedan: equilibrador ↔ arquitecto/materia, imaginador ↔ inesperado, conceptual ↔
atmósferas. Se revisan después de la doble evaluación.

## Próximos pasos

1. Raúl prueba el test en celular y compu, eligiendo distinto cada vez, y manda los PDF.
2. Doble evaluación de vectores con `docs/evaluacion/plantilla_vectores.csv` (ya regenerada con
   las 60 obras nuevas).

## Familia nueva: minimalismo cálido y formas orgánicas (26/09/2026)

Pedido de Raúl: el estilo que más le gusta para su casa (abstracción orgánica en tonos tierra,
planos de color serenos, paisaje brumoso, fotografía de arquitectura en blanco y negro) no
estaba en el test. Es además la tendencia dominante de arte para el hogar en 2026 ("organic
modern", japandi) y el tipo de obra que muestran sus referentes (Nook At You, Musee).

Entraron 8 obras (prefijo MC): Arp, Scully, Rodchenko, Richter (Seascape), Hepworth, Marcela
Cabutti, Martín Reyna y Carola Zech. Salieron: Lozza, Twombly, Kandinsky, Brâncuși, Berni,
Giuliani, Eggleston y Warhol. Descartados por falta de imagen verificable o porque no encajaban
al verlos: Tomie Ohtake, Lucien Hervé, Esteban Pastorino (sus obras son cajas de luz), Juan
Tessi (resultó figurativo).

Ese gusto lo detecta "El coleccionista de atmósferas" (P01), cuyo texto y consejo para la casa se
ampliaron (formas orgánicas, tonos tierra, madera, lino, piedra). Persona "minimalismo cálido" →
atmósferas 75%. Se recalibraron también P06 (imaginador) y P09 (inesperado), que se confundían.
Simulador: ~78% principal, ~91% principal o matiz.

## Ajuste del 28/09/2026: el living de Raúl y las obras que no conectaban

Raúl mostró su living: le gustan especialmente una foto de arquitectura en blanco y negro
(columnas en perspectiva) y una mancha roja suave sobre papel. Se buscaron obras parecidas y
reemplazaron a las que menos ganaban en el F&F (datos de la planilla del 27/09):

| Sale (% de duelos que ganaba) | Entra |
|---|---|
| Josefina Labourt, *Estoy viva* (7%) | Horacio Coppola, *Roque Sáenz Peña* (1936) — FO06 |
| Marina De Caro, cerámica (7%) | Humberto Rivas, *Buenos Aires* (1984) — FO07 |
| Alex Katz, *The Red Smile* (11%) | Adolph Gottlieb, *White Ground–Red Halo* (1966) — CF05 |
| Jean Arp, *Configuration* (17%) | Lee Ufan, *Untitled* (2008) — MC09 |
| Mark Rothko, *No. 61 (Rust and Blue)* | Mark Rothko, *Untitled (Red)* (1956) — CF06 |

Se usaron IDs nuevos (no se reutilizan IDs) para que ningún navegador muestre una imagen vieja
guardada. Simulador: ~80% principal, ~92% principal o matiz. Quedan candidatas a revisar con más
datos: Grete Stern (14%), Le Parc (15%, imagen chica), Doig (17%).
