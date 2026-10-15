# Curaduría 3.0 — plan (catálogo final de 150–200 obras)

Propuesta del 05/10/2026, basada en `docs/INVESTIGACION_COMPETENCIA_Y_TENDENCIAS.md` y en el F&F.

**Decisiones de Raúl (05/10/2026):** 180 obras · poco conocidas: 60% argentinas / 15%
latinoamericanas / 25% internacionales · precio de las poco conocidas USD 500–10.000 ·
**test de 60 duelos** (~10–11 minutos; vigilar el abandono en celular).

## Lo que pidió Raúl

- 150 a 200 obras, todas con imagen de calidad muy buena a excelente.
- Que no todos vean las mismas obras: los duelos se mezclan en cada test.
- Un test al menos el doble de largo, para perfilar mejor.
- Mezcla de **25% obras conocidas o emblemáticas** y **75% poco conocidas** (emergentes, mid-career,
  modernos poco difundidos), con el perfil buscado.
- Incluir sí o sí: fotografía, escultura, hiperrealismo, paisaje natural (playa, montaña, lagos).
- Norte: después se vinculan galerías y talleres con clientes. Nada de obras de precio
  inalcanzable como eje (un Pollock puede estar como referencia, rodeado de emergentes).

## Propuesta de composición (sobre 180 obras)

| Género / lenguaje | % | Obras | Ejemplos de lo que entra |
|---|---|---|---|
| Abstracción (geométrica, color, gestual) | 25% | 45 | Concreto argentino, color field, gesto contemporáneo |
| Minimalismo cálido y formas orgánicas | 10% | 18 | Tonos tierra, formas blandas, monocromos, papel |
| Fotografía (arquitectura, paisaje, calle, retrato) | 17% | 30 | Blanco y negro de arquitectura, mar, montaña, ciudad |
| Paisaje pintado (mar, montaña, lagos, cielos) | 12% | 22 | Paisaje contemporáneo, atmosférico o realista |
| Figuración contemporánea (interiores, retratos, escenas) | 10% | 18 | Pintura figurativa joven, escenas "cálidas" |
| Hiperrealismo | 6% | 11 | Pintura y escultura hiperrealista |
| Escultura y objeto (de apoyo o pared) | 8% | 14 | Escultura chica, relieves, móviles |
| Textil y cerámica | 7% | 12 | Tapiz, bordado, cerámica de pared |
| Pop, gráfica, ilustración e imaginario | 5% | 10 | Pop, obra gráfica, surrealismo contemporáneo |

**Conocidas vs. poco conocidas:** 45 conocidas (25%) y 135 poco conocidas (75%). Las conocidas
reparten los géneros para que la persona se oriente ("esto es tipo Rothko").

**Origen de las 135 poco conocidas ❓:** propuesta 60% argentinas (con galería o taller en CABA),
15% latinoamericanas y 25% internacionales. La parte argentina es la que se puede vender primero.

**Rango de precio de las poco conocidas ❓:** propuesta de foco en obra de **USD 500 a 10.000**
(el rango de entrada del mercado online), con algunas hasta 20.000.

## Cambios en el test

- **Duelos mezclados:** en lugar de 32 duelos fijos, un banco grande (~250 duelos pre-armados con
  las mismas reglas de hoy: familias distintas, fama pareja, contraste) del que cada persona recibe
  una combinación distinta, más una etapa adaptativa que elige los duelos que mejor separan sus dos
  perfiles candidatos.
- **Largo:** **60 duelos** (decisión de Raúl). Con el tiempo medido en el F&F (3,7 s por duelo
  más pausas y preguntas) son unos 10–11 minutos.
- **Perfiles:** con paisaje e hiperrealismo como lenguajes fuertes, evaluar sumar 1 o 2 perfiles
  (por ejemplo, uno de "naturaleza / paisaje"), validando todo con el simulador.
- **Ficha de cada obra (nuevo):** además de los 8 ejes, guardar rango de precio estimado, galería o
  contacto, si es original o edición, y medidas. Es la base para la etapa comercial.
- **Vectores:** con 180 obras, la doble evaluación humana se vuelve pesada. Propuesta: borrador
  hecho por Claude + ajuste con los datos reales de elecciones (con 50–100 personas por obra) +
  revisión humana de las obras dudosas.

## Orden de trabajo propuesto

1. Raúl confirma los ❓.
2. Lista de 180 obras (artista, obra, por qué) por género, en tandas de ~45, para que Raúl pueda
   mirarlas y vetar.
3. Imágenes en buena calidad (mínimo ~1200 px), verificando título y año en la fuente.
4. Fichas y vectores, banco de duelos, test de 60 duelos, simulador.
5. Prueba interna y después lanzamiento.

## Avance

El catálogo 3.0 se arma aparte del test en uso, con `python tools/curaduria_3_0.py` (lista `W`,
reanudable): fichas en `data/v3/artworks.json`, imágenes en `assets/v3/`. Campos nuevos: `Region`
(Argentina / Latinoamérica / Internacional), `Tier` (Conocida / Poco conocida), `Precio_USD`,
`Galeria`. IDs con prefijo de familia y 3 dígitos (AB001, FO005…); familias: AB abstracción,
MC minimalismo cálido, FO fotografía, PA paisaje, FI figuración, HR hiperrealismo, ES escultura,
TX textil y cerámica, PO pop, gráfica e imaginario.

- **Tanda 1 (05/10/2026): 46 obras conocidas — hecha** (aprobada por Raúl). 28 reusadas del 2.0 y
  18 nuevas: Ansel Adams, Cartier-Bresson, Gursky, O'Keeffe, Hopper (*Ground Swell*), Estes (2),
  Chuck Close, Duane Hanson, Ron Mueck, Berni (*Juanito Laguna*), Kahlo, Brâncuși, Giacometti,
  Warhol, Lichtenstein, Haring.
- **Imágenes de la tanda 1 mejoradas (05/10/2026):** 19 de las 20 chicas se reemplazaron por
  versiones de 1500–2500 px (Tate, Cleveland Museum, WikiArt, Wikimedia Commons). En varios casos se
  cambió a otra obra del mismo artista con imagen grande: Rothko *No. 1 (Royal Red and Blue)*, Albers
  *Study for Homage to the Square* (1963), Kelly *Broadway*, Agnes Martin *Morning*, Mitchell
  *Chord II*, Riley *Deny II*, Scully *A Happy Land*, Lee Ufan *With Winds*, Calder *Antennae with
  Red and Blue Dots*, Adnan *Untitled* (2017), Doig *Red Boat*, Kahlo *Las dos Fridas*, Haring
  *Untitled (Dance)*, Kusama *Pumpkin* (acero, 2010), Xul Solar *Ciudá lagui*. Chuck Close → Ralph
  Goings y Sheila Hicks → Magdalena Abakanowicz (no hay imagen grande disponible de los primeros).
  Queda Cartier-Bresson en 821 px.
- **Tandas 2–4 (05/10/2026): 134 obras poco conocidas — hechas.** 80 argentinas, 14
  latinoamericanas y 40 internacionales. Total del catálogo: **180**.
  - Argentinas: 25 reusadas del 2.0 (incluye 7 modernas históricas: Prati, Grilo, Polesello,
    Tomasello, Kosice, Grete Stern, Coppola) + 55 nuevas de galerías de CABA: Ruth Benzacar, Piedras,
    Rolf Art, Del Infinito, Jorge Mara – La Ruche, Gachi Prieto, Hache, Pasto, Barro, Nora Fisch,
    Herlitzka, y el taller de Florencia Trucco. Título, año, técnica y medidas salen de la ficha de
    la galería (verificados), no de memoria.
  - Latinoamericanas: Macaparana, Sclavo, Aramburu, Zé Carlos Garcia, Lucas Simões, Huarcaya,
    Restrepo, Mira Schendel, Lygia Pape, Cruz-Diez, Júlia Martins Miranda, Kamalky Laureano,
    Francisco Mery (2).
  - Internacionales: 36 de Tappan (Los Ángeles; obras a la venta con precio publicado) y 4
    hiperrealistas de FP Art Online (Italia).
  - Composición final (180): abstracción 41, minimalismo cálido 23, fotografía 26, paisaje 19,
    figuración 15, hiperrealismo 11, escultura 17, textil y cerámica 13, pop/imaginario 15.
- **Fichas (paso 5):** todas las poco conocidas tienen `Precio_USD`, `Galeria`, `Formato`
  (Original/Edición) y, cuando la fuente lo dice, `Medidas`. Precios: los de Tappan, FP Art y Trucco
  son los publicados; los de galerías de CABA son **estimados por nivel de carrera, a confirmar**; las
  modernas históricas dicen "20000+ (referencia histórica)".
- **Pendientes de datos:** año desconocido en 49 obras (Tappan y FP no lo publican); 7 sin galería
  (obras históricas o de museo); 34 imágenes entre 550 y 900 px (fotos de producto de Tappan y
  algunas de Pasto/Barro): se ven bien en el celular, pero conviene pedir archivos grandes a las
  galerías antes del lanzamiento.
- Revisión visual para Raúl: `REVISAR_CURADURIA_3_0.html` (abrir en el navegador, filtra por
  región, familia y tipo).

## Etapa B — test de 60 (05/10/2026)

- **Se prueba en paralelo**: `?v=3` al final de la dirección (o `catalog:'v3'` en `config.js`) carga
  `data/v3/` (180 obras, banco de duelos, perfiles propios). Sin eso, el sitio sigue con el test de 24
  del F&F, sin ningún cambio. Para pasar a todos al test nuevo: poner `catalog:'v3'` en `config.js`.
- **Banco de duelos** (`tools/armar_duelos_v3.py --escribir` → `data/v3/duels.json`): 273 duelos,
  cada obra en 3, familias y artistas distintos, fama pareja, contraste mínimo 3,7 (promedio 6,5).
- **Recorrido**: 36 duelos sorteados por persona (sin repetir obra ni familia seguida) + 24
  adaptativos. Preguntas en los duelos 10, 20, 30, 40, 50, 55 y al final; pausas cada 12; "¿La
  tendrías en tu casa?" en 15, 35 y 50. El progreso guardado incluye el sorteo (`plan`).
- **Perfiles del test 60** (`data/v3/profiles.json`, el test de 24 no cambia): P03 y P08
  recalibrados por simulación; P05 pasa a "El observador de lo real" (incluye paisaje e
  hiperrealismo, que en la simulación caían ahí). Textos nuevos de P03 y P05 a revisar por Raúl.
- **Simulación** (Edge headless, 1800 usuarios por perfil + personas): **88,9% principal, 96,4%
  principal o matiz, máximo 15% al azar**. Raúl (abstracción serena) → atmósferas 86%, arquitecto 11%,
  equilibrador 4%. Paisaje y realismo → observador de lo real. Con los perfiles viejos daba 77,7% / 88,5%.
- **Planilla**: columna nueva `catalogo` (v2/v3) y el mail dice "los N duelos". Requiere publicar
  `Code.gs` (New version).

## Infraestructura antes de difundir (pedido de Raúl)

- **Pasar a Vercel y hacer privado el repositorio.** Orden importante: primero Vercel, después
  privado. GitHub Pages gratis sólo funciona con repositorios públicos: si se hace privado primero,
  la web se cae. Vercel puede publicar desde un repositorio privado.
- El plan gratuito de Vercel (Hobby) es para uso no comercial; cuando haya ventas, corresponde el
  plan Pro (USD 20 por mes). Para la etapa actual alcanza el gratuito.
- Al mudar: actualizar `imagesBaseUrl` en `config.js` a la dirección nueva.
