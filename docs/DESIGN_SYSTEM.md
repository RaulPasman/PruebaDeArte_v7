# Design system — Prueba de Arte

Este documento describe el sistema visual que ya está construido en `styles.css`, `index.html`
y `app.js` — no propone una estética nueva. Es la referencia para mantener todo lo que se
agregue de acá en adelante (nuevas pantallas, el mail, futuros materiales) consistente con lo
que ya existe. Para verlo en vivo, con los componentes reales renderizados, abrí
`DESIGN_SYSTEM.html` (junto a este archivo) con un servidor local — usa el `styles.css` real
del proyecto, así que si el CSS cambia, la guía se actualiza sola.

## En una frase

**Sala de museo minimalista, no app de SaaS.** Fondo hueso, tipografía editorial serif para lo
que importa, texto de sistema en sans-serif chico y tracked, cero esquinas redondeadas, líneas
finas en vez de sombras, y un solo acento: negro sólido. La obra siempre es la protagonista —
el sistema se corre atrás.

## Color

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#f3f3ef` | Fondo general (hueso, no blanco puro) |
| `--paper` | `#ffffff` | Tarjetas, formularios, fondo de imágenes |
| `--ink` | `#171717` | Texto principal |
| `--dark` | `#111111` | Botones primarios, acentos fuertes, puntos de los gráficos de eje |
| `--muted` | `#777777` | Texto secundario, metadatos |
| `--soft` | `#9a9a95` | Texto terciario, eyebrows sobre fondo claro |
| `--line` | `#d9d9d3` | Divisores, bordes de sección |

Grises adicionales que aparecen en el CSS, todos dentro de la misma familia cálida (nunca gris
azulado): `#555` `#666` `#888` `#999` `#aaa` `#bbb` `#ccc` `#ddd` `#d4d4d0` `#e4e4df` `#e5e5e0`
`#e7e7e2` `#eee` — se usan según cuánto contraste necesita ese texto o borde puntual, no hay
una escala numerada estricta (50/100/200...); es una paleta orgánica de grises cálidos.

**Único color de acento: negro.** No hay un color "de marca" tipo terracota o azul — la
distinción viene de la tipografía y el espaciado, no de un color llamativo. Si en algún
momento hace falta un color de estado (error), se usa `#b3261e` (rojo apagado, no un rojo de
alerta genérico) — es el único color no neutro en todo el sistema. Está reservado para errores
de formulario nada más.

## Tipografía

Dos familias, cada una con un trabajo fijo — nunca se mezclan dentro del mismo elemento:

- **Georgia, serif** — títulos, nombres de obra, narrativa del resultado, cualquier texto que
  el usuario tiene que sentir, no sólo leer. Peso 500 (nunca bold real, nunca 400 en los
  títulos grandes), interlineado ajustado (`.98`–`1.15`) y letter-spacing negativo en los
  títulos grandes (`-0.04em` a `-0.045em`) para que la escala grande no se sienta suelta.
- **Arial, Helvetica, sans-serif** — todo lo demás: cuerpo de la interfaz, botones, labels,
  metadatos, formularios. Es la voz "del sistema", nunca la voz "de la obra".

### Escala

| Uso | Tamaño | Familia / peso | Ejemplo en código |
|---|---|---|---|
| H1 de pantalla completa | `clamp(42px,7vw,82px)` / línea `.98` | Georgia 500, `-.045em` | `.intro h1` |
| H1 de resultado | `clamp(44px,7vw,82px)` / línea `1` | Georgia 500, `-.04em` | `.result h1` |
| Título de sección | `36px` | Georgia 500 | `.section-head h2` |
| Título de duelo / obra en foco | `38–42px` | Georgia 500 | `.duel-intro h2`, `.pause-work h2` |
| Título de tarjeta de obra | `18px` | Georgia normal | `.work-info strong` |
| Cuerpo largo / narrativa | `18px` / línea `1.6–1.7` | Georgia | `.narrative`, `.intro p` |
| Cuerpo de UI | `14–16px` | Arial | formularios, mail |
| Eyebrow (label superior) | `10–11px`, tracking `.16–.22em`, mayúsculas | Arial | `.eyebrow` |
| Micro / metadatos | `10–12px` | Arial, gris | `.micro`, `.hint`, `.q-progress` |

**Regla práctica:** si es algo que el usuario elige o siente (un título, el nombre de una obra,
el resultado), va en Georgia. Si es algo que el sistema le dice para orientarlo (un progreso,
un label, un botón), va en Arial, chico y tracked si es una etiqueta.

## Espaciado y layout

- **Sin sistema numerado de espaciado** (no hay una escala 4/8/12/16px estricta) — los valores
  se ajustan al contenido de cada bloque, pero todos caen en el rango 8px–70px, con los saltos
  grandes (45–70px) reservados para separar secciones completas.
- **Anchos de contenido según la pantalla:**
  - `940px` — pantallas de una sola columna centrada (intro, identidad, preguntas, pausas)
  - `1200px` — resultado y exploración
  - `1500px` — duelos (necesitan más aire para las dos obras)
  - `480–820px` — bloques de texto/formulario dentro de una pantalla más ancha (nunca el texto
    ocupa todo el ancho de un layout grande)
- **Grillas:** 2 columnas para comparar (duelo, `result-grid`, `pause-work`), 3 columnas para
  galerías (`work-grid`, `artist-mini-grid`), 5 columnas sólo para los pasos numerados de
  exploración (`steps`). Todas colapsan a 1–2 columnas debajo de 800px.

## Componentes

### Botones
- **Primario:** fondo `#111`, texto blanco, sin borde, sin radio, `padding:14px 23px`. Hover:
  `translateY(-1px)` + fondo `#2b2b2b`. Es el único botón "sólido" del sistema — se usa para la
  acción principal de cada pantalla, nunca más de uno por pantalla.
- **Secundario / outline:** transparente, borde `1px solid #bbb`, texto `#555`. Hover: borde y
  texto pasan a `#111` (nunca cambia el fondo). Se usa para "Ambas", "Ninguna", "volver",
  acciones que no son el camino principal ("No estoy seguro" también).
- **Botón de texto:** sin borde ni fondo, en el estilo del eyebrow (mayúsculas, tracked). Se usa
  para "← Anterior" en el encabezado del duelo, para que volver atrás no compita con elegir.
- **Opción de encuesta (feedback):** mismo esqueleto que el secundario, pero al seleccionarse
  se invierte a fondo `#111` / texto blanco — el único lugar donde un botón outline "se llena"
  como estado, no como hover.

### Tarjetas de obra
Nunca tienen borde ni sombra — se separan por espacio en blanco y por el propio contraste de
la imagen contra `--bg`. En galerías y resultado el contenedor de imagen es `aspect-ratio:4/3`;
en el duelo no tiene proporción fija: se estira para llenar el alto de la pantalla (así las dos
obras y los botones entran sin scrollear, también en celular). Siempre `object-fit:contain`
sobre fondo `#eee`/`#e5e5e0` (nunca recorta la obra). El texto debajo es
mínimo: nombre en Georgia 18px, metadato en Arial 10-12px tracked.

### Placeholder de imagen faltante
Fondo gris (`#e5e5e0`), un ícono/texto centrado en Georgia 22px con un label Arial debajo en
mayúsculas. **Nunca debe mostrar el título real de la obra** cuando se usa dentro de un duelo
(rompería el ejercicio de elegir "a ciegas") — esto es una regla de producto, no sólo visual.

### Formularios
Inputs sin caja: `border:0; border-bottom:1px solid #aaa`, fondo transparente. El label va
arriba, chico, tracked, mayúsculas (Arial 11px). Foco: `outline:2px solid #111` con offset —
nunca el borde de color azul del navegador por defecto. Error: texto `#b3261e`, 13px, aparece
debajo del campo, nunca como un cartel/toast.

### Barra de progreso
`height:2px`, fondo `#ddd`, relleno `#111` con transición de ancho. Minimalista a propósito:
no es una barra "gamificada" con porcentaje grande, es una línea fina que confirma que hay un
final.

### Visualización de ejes (resultado)
Una línea de 1px (`#c9c9c4`) con un punto circular de 7px (`#111`) posicionado según el valor
del eje. Nada de gráficos de barra tradicionales ni colores por categoría — es deliberadamente
austero, como una ficha técnica de museo.

### Eyebrow / etiquetas
`10-11px`, `letter-spacing:.16-.22em`, mayúsculas, color `#777`–`#9a9a92`, siempre arriba a la
izquierda de un bloque. Es el recurso tipográfico que más se repite en todo el sistema — hace
las veces de "kicker" editorial.

### Divisores
Siempre `1px solid var(--line)`, nunca sombras ni degradados para separar secciones.

## Movimiento

Deliberadamente contenido: `translateY(-1px)` en hover de botones y tarjetas, transición de
`.15s` a `.45s`, y un único efecto "vivo" — el zoom sutil (`scale(1.012)`) de la imagen al
pasar el mouse sobre una obra. No hay animaciones de entrada, fade-ins en scroll, ni
transiciones decorativas — el movimiento siempre responde a una acción del usuario, nunca es
ambiental.

## Esquinas y bordes: cero radio, siempre

En todo `styles.css` no hay un solo `border-radius` (fuera de los puntos circulares de los
ejes, que son parte del gráfico, no del chrome). Es una decisión, no un olvido: refuerza el
carácter de ficha/etiqueta de museo en vez de "producto de software". **Si se agrega un
componente nuevo, no le pongas esquinas redondeadas** salvo que sea otro elemento circular
como los puntos de eje.

## Voz y contenido

- Segunda persona, tono directo pero cálido ("Elegí por intuición", "Sin pensar demasiado").
- Los mensajes de error explican qué pasó y qué hacer, sin culpar ("Revisá el mail: lo
  necesitamos para enviarte tu resultado" — no "Email inválido").
- Los eyebrows son sustantivos cortos en mayúsculas ("TU OPINIÓN · 30 SEGUNDOS",
  "ANTES DE EMPEZAR"), nunca frases largas.
- Nada de signos de exclamación salvo en confirmaciones breves ("¡Gracias!").

## Extensión: el mail y el PDF (`apps_script/Code.gs`)

El mail de resultado y el PDF adjunto usan el mismo lenguaje, adaptado a lo que un cliente de
correo soporta (sin `aspect-ratio`, sin grid, todo con tablas e inline styles):

- Mismo fondo hueso (`#f3f3ef`) con una "tarjeta" blanca centrada, borde `1px solid #e3e2da`.
- Mismo Georgia para el nombre del perfil (36-46px) y Arial para eyebrow/metadatos.
- Mismo botón sólido negro para el único CTA ("Volver a Prueba de Arte").
- Mismo tono de gris apagado para el subtítulo en itálica.

Si se rediseña la web, este es el otro lugar donde hay que replicar el cambio a mano (no
comparten CSS por las limitaciones de los clientes de mail).

## Qué evitar

- Un segundo color de acento (nada de terracota, azul, verde — el sistema es monocromático a
  propósito).
- Esquinas redondeadas en tarjetas, botones o inputs.
- Sombras (`box-shadow`) para dar profundidad — usar espacio o líneas finas.
- Mayúsculas en texto largo (sólo en eyebrows y labels cortos).
- Mezclar Georgia y Arial dentro del mismo bloque de texto.
- Animaciones que no respondan a una acción del usuario.
