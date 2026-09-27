# Friends & Family — análisis de resultados

Raúl va guardando los PDF de resultado en `C:\Users\RaulPasman\Desktop\F&F - Prueba de arte`.
Cuando pida "analizá los nuevos", analizar **sólo los archivos que no estén en el registro de abajo**,
y después agregarlos al registro con la fecha.

Hay dos tipos de PDF: "Tu mirada artistica - X.pdf" (el que llega por mail) y "Prueba de Arte -
X.pdf" (la página del resultado impresa desde el navegador). Los dos traen perfil, matices, ejes,
selección y recomendaciones, pero **no** los duelos uno por uno: para eso hace falta la planilla
(hojas Sesiones y Eventos).

## Registro de PDF analizados

### Tanda 1 — analizada el 27/09/2026 (12 personas)

| Archivo | Perfil | Matices |
|---|---|---|
| Prueba de Arte - Alejandra Ferhmin.pdf | Arquitecto visual | Equilibrador |
| Tu mirada artistica - MAURO.pdf | Arquitecto visual | Atmósferas · Conceptual |
| Prueba de Arte - Juanfri.pdf | Cazador de lo inesperado | — |
| Tu mirada artistica - Julian.pdf | Explorador conceptual | — |
| Prueba de Arte - Ignacio Melero.pdf | Coleccionista de atmósferas | Arquitecto |
| Tu mirada artistica - Juan Dujovne.pdf | Arquitecto visual | Atmósferas |
| Tu mirada artistica - Juamba.pdf | Explorador conceptual | — |
| Prueba de Arte - Alfredo.pdf | Coleccionista de atmósferas | Conceptual · Arquitecto · Imaginador |
| Tu mirada artistica - Lucas Cairella.pdf | Observador de lo cotidiano | Materia · Intensidad |
| Prueba de Arte - Isidro.pdf | Coleccionista de atmósferas | Arquitecto |
| Tu mirada artistica - Catalina.pdf | Buscador de intensidad | Materia |
| Tu mirada artistica - Iñaki Kasangian.pdf | Arquitecto visual | Cotidiano · Atmósferas |

## Hallazgos de la tanda 1

1. **Reparto de perfiles razonable** (ninguno pasa de 4 de 12): arquitecto 4, atmósferas 3,
   conceptual 2, inesperado 1, cotidiano 1, intensidad 1. No apareció nunca como principal:
   materia, equilibrador, imaginador ni explorador sin fronteras. Con 12 personas no alcanza
   para sacar conclusiones; seguirlo en las próximas tandas.
2. **Público calmo y ordenado**: arquitecto + atmósferas = 7 de 12. Coincide con lo que
   anticipaba el relevamiento (abstracción serena, fotografía, minimalismo cálido). Obras más
   elegidas: Saul Leiter *Red Umbrella* (7 de 12), Rodchenko *Stairway* (5), Duville *Trayecto*
   (5), Mondrian (4). La fotografía gusta mucho.
3. **Problema: recomendaciones casi iguales para todos.** Macchi *Buenos Aires Tour* salió
   recomendada a 11 de 12; Asawa, Pombo, Alarcón y Zech a 8–9. Causa: la etapa adaptativa elegía
   siempre los mismos duelos del banco (simulador: 5 duelos al 100% de las personas, 7 al 0%),
   así que todos veían casi las mismas obras y las no vistas eran siempre las mismas.
   **Corregido** (ver abajo).
4. **Problema: la frase "en tus elecciones pesaron…" a veces contradecía al perfil** (Catalina:
   "buscador de intensidad" con "lo cotidiano, lo espontáneo y lo transparente"). **Corregido.**
5. Catalina salió "intensidad" con una selección más bien calma (Adnan, Gurfein, Hicks): el perfil
   de intensidad se lleva a quien elige mucho lo "espontáneo". Con la nueva etapa adaptativa
   debería recibir duelos que separen intensidad de materia. Vigilar.

## Cambios aplicados el 27/09/2026 (versión 2.0.2)

- **Duelos adaptativos de verdad** (`adaptiveDuel()` en `app.js`): después de los 16 fijos, el
  test mira los dos perfiles entre los que duda para esa persona y elige el duelo que mejor los
  separa. Simulador: el uso del banco pasó de "todo o nada" a entre 32% y 85% por duelo; la obra
  más recomendada bajó del 75% al 57% de las personas; acierto sin cambios (~78% / ~91%).
- **Frase de ejes coherente con el perfil** (`narrative()`): prioriza los ejes que explican el
  perfil asignado.

## Planilla del 27/09/2026 (`Sheet 270926 0122.xlsx`, en la carpeta del F&F)

17 sesiones reales (sin contar las marcadas como prueba):
- **16 terminaron el test**, 1 abandonó (en el duelo 14). 12 de 17 desde el **celular**.
- **Duración mediana: 3,2 minutos** (rango 1,8–48). Mucho menos que los 5–8 que promete la portada.
- **Sólo 6 de 16 contestaron la encuesta final (38%)** y **nadie hizo la ruta de 5 pasos (0 de 16)**.
  Raúl también lo notó: la gente no ve todo lo que viene después del perfil.
- Encuesta (6 respuestas): acierto 3/5 (4 personas), 2 y 4 (una cada una); "¿descubriste algo?":
  un poco 4, no 2; "¿querés ver obras así para tu casa?": sí 2, tal vez 2, no 2.
- **Prueba de perfil: 8 de 11 eligieron la descripción de su propio perfil** (73%; al azar sería
  50%). Buena señal de que el perfil describe a la persona.
- "¿La tendrías en tu casa?": respondido en todas las sesiones; la mayoría dice sí a 2 o 3 de 3.

**Cambio (versión 2.0.3):** el resultado pasó a ser un recorrido guiado de 5 pantallas
(Perfil · Obras · Casa · Opinión · Seguí mirando), con barra de pasos arriba y un botón que dice
qué viene. La encuesta tiene su propia pantalla (con "Saltear"), el texto "mirá esto" de cada obra
quedó visible, y la pared de obras pasó a la pantalla de la casa. Se registra hasta qué pantalla
llega cada persona (eventos `result_step`, `route_start`, `route_step` en la hoja Eventos).

## Para la próxima tanda

- Medir con la planilla nueva: % que llega a cada pantalla (evento `result_step`), % que contesta
  la encuesta y % que empieza la ruta. Antes: encuesta 38%, ruta 0%.

- Pedir a Raúl que descargue la planilla (Archivo → Descargar → Microsoft Excel) y la guarde en
  la misma carpeta: con las hojas **Sesiones** y **Eventos** se puede ver cada duelo, cuánto
  tardó cada persona, dónde abandonó, qué contestó en "¿La tendrías en tu casa?", la prueba de
  perfil (si reconoce el suyo) y la encuesta final (acierto 1–5). Es mucha más información que
  los PDF.
- Comparar el reparto de perfiles antes y después del cambio de la etapa adaptativa (los PDF
  del 27/09 en adelante ya usan la versión 2.0.2 si la persona entró después del push).
