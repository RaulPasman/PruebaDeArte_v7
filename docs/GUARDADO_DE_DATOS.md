# Guardado de datos en Google Sheets — guía paso a paso

Tiempo estimado: 15–20 minutos, una sola vez. No hace falta saber programar.

## Qué vas a obtener
Una planilla de Google con tres hojas:
- **Sesiones**: una fila por persona (mail, dispositivo, estado, último paso, perfil, matices, duración, opinión, reflexión, si se le envió el mail). Si alguien abandona, ves en qué duelo.
- **Eventos**: el detalle de cada paso (cada duelo con la obra elegida y el tiempo que tardó).
- **Errores**: sólo por si algo llega mal (debería quedar vacía).

Además, cada persona que termina recibe su perfil por mail.

## Recomendación previa
Creá la planilla desde una cuenta de Gmail dedicada al proyecto (por ejemplo `pruebadearte…@gmail.com`). Los mails de resultado salen desde esa cuenta, no desde tu mail personal.

## Paso 1 · Crear la planilla
1. Entrá a https://sheets.new con la cuenta elegida.
2. Poné de nombre: **Prueba de Arte — Resultados**.

## Paso 2 · Pegar el código
1. En la planilla: menú **Extensiones → Apps Script**.
2. Borrá todo lo que aparece en el editor.
3. Abrí `apps_script/Code.gs` con el Bloc de notas, copiá todo y pegalo en el editor.
4. Guardá (ícono de disquete o Ctrl+S).

## Paso 3 · Ejecutar "configurar" (crea las hojas y pide permisos)
1. Arriba del editor, en el desplegable de funciones, elegí **configurar** y tocá **Ejecutar**.
2. Va a pedir autorización: **Revisar permisos** → elegí tu cuenta.
3. Aparece "Google no verificó esta app". Es normal: la app es tuya. Tocá **Configuración avanzada → Ir a … (no seguro) → Permitir**.
4. Volvé a la planilla: tienen que aparecer las hojas **Sesiones**, **Eventos** y **Errores** con encabezados.

## Paso 4 · Publicar el receptor
1. En el editor de Apps Script: **Implementar → Nueva implementación**.
2. En el engranaje, elegí **Aplicación web**.
3. Descripción: `v1`. **Ejecutar como: Yo**. **Quién tiene acceso: Cualquier usuario**.
4. **Implementar** → copiá la **URL de la aplicación web** (termina en `/exec`).
5. Pegala en el navegador: tiene que decir "Prueba de Arte: receptor activo."

## Paso 5 · Conectar la app
1. Abrí `config.js` con el Bloc de notas.
2. Pegá la URL entre las comillas: `webhookUrl: "https://script.google.com/macros/s/…/exec"`.
3. Guardá.

## Paso 6 · Probar
1. Doble clic en `ABRIR_PRUEBA_DE_ARTE.bat` y hacé el test completo con tu mail.
2. En la planilla tiene que aparecer tu fila, completándose a medida que avanzás, con **es_prueba = sí**.
3. Al llegar al resultado te tiene que llegar el mail (revisá también Spam la primera vez).

## Cómo distinguir pruebas de usuarios reales
Todo lo que se hace desde tu PC (localhost) o con `?test=1` al final del link queda marcado **es_prueba = sí**. Tus amigos, desde el link publicado, quedan sin marca. Filtrá esa columna para analizar.

## Si cambiás el código de la planilla más adelante
**Implementar → Administrar implementaciones → lápiz → Versión: Nueva versión → Implementar.** Así la URL se mantiene y no tenés que tocar `config.js`. (Si hacés "Nueva implementación" cambia la URL.)

## Límites y cuidados
- Gmail permite alrededor de 100 mails por día desde Apps Script con una cuenta común: sobra para el F&F.
- La URL del receptor queda visible en el código de la página. Para un F&F no es un problema; alguien podría mandar datos basura, y quedarían en la hoja Errores o como filas sueltas.
- Si `config.js` queda vacío, la prueba funciona igual pero no guarda nada.

## Si te aparece "Sorry, unable to open the file at this time" (pantalla de Google Drive)

Es un error conocido de Google, no algo que hayas hecho mal. La causa más común, por lejos:
**tenés más de una cuenta de Google abierta en el navegador**, y Apps Script intenta abrir el
proyecto con la cuenta que no es.

**Solución (funciona en la mayoría de los casos):**
1. Abrí una ventana de **incógnito** (Ctrl+Shift+N en Chrome).
2. Entrá a https://sheets.google.com e iniciá sesión **solo** con la cuenta donde creaste la
   planilla.
3. Abrí tu planilla y repetí: **Extensiones → Apps Script**.

Si con eso no alcanza, dos alternativas:
- Cerrá sesión de todas las demás cuentas de Google en el navegador (no sólo cambiar de cuenta
  activa) y volvé a intentar.
- Probá desde otro navegador donde sólo tengas esa cuenta iniciada.

### Plan B: crear el script por separado (si el error persiste)

Si después de probar lo anterior seguís trabada, se puede crear el script sin pasar por
"Extensiones" de la planilla:

1. Andá a **https://script.new** (con la cuenta correcta, e idealmente en la misma ventana de
   incógnito del paso anterior).
2. Se abre un proyecto de Apps Script nuevo y vacío. Borrá el contenido y pegá `Code.gs` igual
   que en el Paso 2 de la guía principal.
3. Abrí tu planilla, copiá el **ID de la planilla**: es la parte de la URL entre `/d/` y `/edit`.
   Por ejemplo, en `https://docs.google.com/spreadsheets/d/1AbCdEfGhIjK.../edit`, el ID es
   `1AbCdEfGhIjK...`.
4. En el editor de Apps Script, al principio del código, pegá ese ID en la línea:
   `const SHEET_ID = '1AbCdEfGhIjK...';`
5. Guardá y seguí desde el **Paso 3** de la guía principal (ejecutar "configurar", etc.) con
   normalidad.

La única diferencia de este camino es esa línea `SHEET_ID`; todo lo demás (publicar como
aplicación web, copiar la URL, pegarla en `config.js`) es exactamente igual.
