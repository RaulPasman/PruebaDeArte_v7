/**
 * Prueba de Arte — receptor de datos en Google Sheets.
 *
 * Qué hace:
 *  - Hoja "Sesiones": una fila por persona que hace el test (se va actualizando a medida que avanza).
 *  - Hoja "Eventos": registro detallado de cada paso (cada duelo, pregunta, resultado, opinión).
 *  - Al terminar, envía por mail el perfil a la persona (desde tu cuenta de Gmail).
 *
 * Instalación (una sola vez): ver docs/GUARDADO_DE_DATOS.md
 *   1) Pegar este código en Extensiones > Apps Script.
 *   2) Ejecutar la función "configurar" y autorizar.
 *   3) Implementar > Nueva implementación > Aplicación web
 *      (Ejecutar como: yo · Quién tiene acceso: cualquier usuario).
 *   4) Copiar la URL que termina en /exec y pegarla en config.js.
 */

const ENVIAR_MAIL_RESULTADO = true;       // poné false si no querés que se envíe el mail

// Dejalo vacío si pegaste el código desde Extensiones > Apps Script (script "vinculado" a esta planilla).
// Si en cambio creaste el proyecto en script.new (script "independiente"), pegá acá el ID de la
// planilla: es la parte de la URL entre /d/ y /edit, por ejemplo
// https://docs.google.com/spreadsheets/d/ESTE_ES_EL_ID/edit
const SHEET_ID = '';
const NOMBRE_REMITENTE = 'Prueba de Arte';
const HOJA_SESIONES = 'Sesiones';
const HOJA_EVENTOS = 'Eventos';
const HOJA_ERRORES = 'Errores';

const COLS_SESIONES = [
  'session_id', 'inicio', 'actualizado', 'es_prueba', 'nombre', 'email', 'consentimiento',
  'dispositivo', 'estado', 'ultimo_paso', 'duelos_respondidos', 'perfil', 'matices',
  'ejes_principales', 'duracion_min', 'acierto_1a5', 'descubrio_algo', 'quiere_ver_obras',
  'comentario', 'reflexion', 'mail_enviado', 'respuestas_json',
  // Agregadas el 26/09/2026 (siempre al final, para no correr las columnas viejas):
  'grupo_prueba_perfil', 'prueba_perfil', 'la_tendria_en_casa'
];
const TEXTO_PRUEBA_PERFIL = { own: 'eligió el suyo', other: 'eligió el otro', none: 'ninguna de las dos' };
const COLS_EVENTOS = [
  'fecha', 'session_id', 'es_prueba', 'tipo', 'paso', 'duelo', 'obra_a', 'obra_b',
  'eleccion', 'ms', 'detalle'
];

/** Ejecutar una vez desde el editor para crear las hojas y los encabezados. */
function configurar() {
  const ss = getSS_();
  prepararHoja_(ss, HOJA_SESIONES, COLS_SESIONES);
  prepararHoja_(ss, HOJA_EVENTOS, COLS_EVENTOS);
  prepararHoja_(ss, HOJA_ERRORES, ['fecha', 'error', 'contenido']);
  // Pide el permiso de envío de mails ahora, así no falla la primera vez.
  if (ENVIAR_MAIL_RESULTADO) MailApp.getRemainingDailyQuota();
  SpreadsheetApp.flush();
}

function getSS_() {
  return SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
}

function prepararHoja_(ss, nombre, cols) {
  const sh = ss.getSheetByName(nombre) || ss.insertSheet(nombre);
  sh.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold').setBackground('#f1f0ea');
  sh.setFrozenRows(1);
  return sh;
}

/** Permite comprobar desde el navegador que la URL funciona. */
function doGet() {
  return ContentService.createTextOutput('Prueba de Arte: receptor activo.');
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  let raw = '';
  try {
    lock.waitLock(25000);
    raw = (e && e.postData && e.postData.contents) || '';
    const d = JSON.parse(raw);
    if (!d || typeof d.session_id !== 'string' || d.session_id.length > 64 || !d.type) {
      throw new Error('payload inválido');
    }
    const ss = getSS_();
    registrarEvento_(ss, d);
    actualizarSesion_(ss, d);
    return ContentService.createTextOutput('ok');
  } catch (err) {
    try {
      const ss = getSS_();
      const sh = ss.getSheetByName(HOJA_ERRORES) || prepararHoja_(ss, HOJA_ERRORES, ['fecha', 'error', 'contenido']);
      sh.appendRow([new Date(), String(err), recortar_(raw, 2000)]);
    } catch (ignored) {}
    return ContentService.createTextOutput('error');
  } finally {
    try { lock.releaseLock(); } catch (ignored) {}
  }
}

function registrarEvento_(ss, d) {
  const sh = ss.getSheetByName(HOJA_EVENTOS) || prepararHoja_(ss, HOJA_EVENTOS, COLS_EVENTOS);
  const detalle = Object.assign({}, d);
  ['v', 'session_id', 'type', 'test', 'ts', 'n', 'duel', 'a', 'b', 'choice', 'ms', 'answers', 'narrative', 'email']
    .forEach(k => delete detalle[k]);
  const eleccion = { A: 'A', B: 'B', both: 'Ambas', neither: 'Ninguna', unsure: 'No estoy seguro' }[d.choice] || '';
  sh.appendRow([
    new Date(), d.session_id, d.test ? 'sí' : '', d.type, d.n || '', d.duel || '',
    d.a || '', d.b || '', eleccion, d.ms == null ? '' : d.ms,
    recortar_(JSON.stringify(detalle), 5000)
  ]);
}

function actualizarSesion_(ss, d) {
  let sh = ss.getSheetByName(HOJA_SESIONES) || prepararHoja_(ss, HOJA_SESIONES, COLS_SESIONES);
  // Si se agregaron columnas nuevas al código, completa los encabezados que falten.
  if (sh.getLastColumn() < COLS_SESIONES.length) sh = prepararHoja_(ss, HOJA_SESIONES, COLS_SESIONES);
  const fila = buscarFila_(sh, d.session_id);
  const actual = fila ? leerFila_(sh, fila) : {};
  const u = { session_id: d.session_id, actualizado: new Date(), es_prueba: d.test ? 'sí' : '' };

  switch (d.type) {
    case 'start':
      Object.assign(u, {
        inicio: new Date(), nombre: recortar_(d.name, 120), email: recortar_(d.email, 200),
        consentimiento: d.consent ? 'sí' : 'no', estado: 'iniciado', ultimo_paso: 'identificación',
        duelos_respondidos: 0,
        grupo_prueba_perfil: d.pt_group ? 'sí' : 'no',
        dispositivo: d.device ? (d.device.mobile ? 'celular' : 'computadora') + ' ' + d.device.width + 'x' + d.device.height : ''
      });
      break;
    case 'duel':
      if (actual.estado !== 'terminado') { u.estado = 'en curso'; u.ultimo_paso = 'duelo ' + d.n; }
      u.duelos_respondidos = Math.max(Number(actual.duelos_respondidos || 0), Number(d.n || 0));
      break;
    case 'question':
      if (actual.estado !== 'terminado') u.ultimo_paso = 'pregunta ' + d.q;
      break;
    case 'result':
      Object.assign(u, {
        estado: 'terminado', ultimo_paso: 'resultado', perfil: d.profile || '',
        matices: (d.nuances || []).join(' · '), ejes_principales: (d.axes || []).join(' · '),
        duracion_min: d.minutes == null ? '' : d.minutes,
        duelos_respondidos: (d.answers || []).length,
        respuestas_json: recortar_(JSON.stringify({ answers: d.answers, questions: d.questions, values: d.values,
          home_answers: d.home_answers, profile_test: d.profile_test }), 45000)
      });
      if (d.home_answers && d.home_answers.length) u.la_tendria_en_casa = resumenCasa_(d.home_answers);
      if (d.profile_test && d.profile_test.chose) u.prueba_perfil = textoPruebaPerfil_(d.profile_test);
      if (!actual.email && d.email) u.email = recortar_(d.email, 200);
      if (ENVIAR_MAIL_RESULTADO && !actual.mail_enviado) u.mail_enviado = enviarMail_(d, actual);
      break;
    case 'feedback':
      Object.assign(u, {
        acierto_1a5: d.rating || '', descubrio_algo: d.discovered || '',
        quiere_ver_obras: d.wants_works || '', comentario: recortar_(d.comment, 1500)
      });
      break;
    case 'reflection':
      u.reflexion = recortar_(d.text, 1500);
      break;
    case 'home':
      // Se va acumulando por si la persona abandona antes del resultado; el resultado lo reescribe completo.
      u.la_tendria_en_casa = recortar_((actual.la_tendria_en_casa ? actual.la_tendria_en_casa + ' · ' : '') +
        d.work + ': ' + d.answer, 300);
      break;
    case 'profile_test':
      u.prueba_perfil = textoPruebaPerfil_(d);
      break;
  }
  escribirFila_(sh, fila, Object.assign({}, actual, u));
}

function enviarMail_(d, actual) {
  const to = d.email || actual.email;
  if (!to || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(to)) return 'sin mail';
  const nombre = (d.name || actual.nombre || '').trim();
  const primerNombre = nombre.split(' ')[0] || '';
  const cuerpo = cuerpoMail_(d, nombre, primerNombre);
  let attachments = [];
  try {
    const pdfHtml = pdfPerfilHtml_(d, nombre);
    const pdf = Utilities.newBlob(pdfHtml, MimeType.HTML)
      .getAs(MimeType.PDF)
      .setName('Tu mirada artistica' + (primerNombre ? ' - ' + primerNombre : '') + '.pdf');
    attachments = [pdf];
  } catch (err) {
    // Si por algo falla la generación del PDF, el mail sale igual, sin adjunto.
  }
  try {
    MailApp.sendEmail({
      to: to,
      subject: 'Tu mirada artística' + (primerNombre ? ', ' + primerNombre : '') + ' 🎨',
      htmlBody: cuerpo,
      name: NOMBRE_REMITENTE,
      attachments: attachments
    });
    return 'sí';
  } catch (err) {
    return 'error: ' + String(err).slice(0, 120);
  }
}

// Cuerpo del mail: cálido, con aire, pensado para leerse cómodo en el celular.
// Bloque con miniatura de cada obra (si hay imagesBaseUrl) o lista de texto simple si no.
function bloqueObras_(titulo, items, textos, baseUrl, imgSize) {
  const hayItems = items && items.length;
  if (!hayItems && (!textos || !textos.length)) return '';
  const etiqueta = '<p style="font:12px Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;' +
    'color:#8a8a84;margin:0 0 12px">' + html_(titulo) + '</p>';
  if (baseUrl && hayItems) {
    const filas = items.map(x =>
      '<tr>' +
      '<td width="' + imgSize + '" style="padding:0 14px 14px 0;vertical-align:top">' +
      '<img src="' + html_(baseUrl + x.id + '.jpg') + '" width="' + imgSize + '" ' +
      'style="display:block;width:' + imgSize + 'px;max-width:' + imgSize + 'px;height:auto;' +
      'border:1px solid #e3e2da"></td>' +
      '<td style="padding:0 0 14px;vertical-align:middle;font:15px/1.4 Georgia,serif;color:#333">' +
      html_(x.label) + '</td>' +
      '</tr>'
    ).join('');
    return etiqueta + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">' + filas + '</table>';
  }
  // Sin imagesBaseUrl configurada (o sin datos de ID): texto simple, como antes.
  const lista = (textos || []).map(x =>
    '<div style="padding:5px 0;font:16px/1.5 Georgia,serif;color:#333">' + html_(x) + '</div>'
  ).join('');
  return etiqueta + lista;
}

function cuerpoMail_(d, nombre, primerNombre) {
  const baseUrl = d.imagesBaseUrl || '';

  return `<div style="background:#f3f3ef;padding:32px 14px;font-family:Georgia,'Times New Roman',serif">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e3e2da">
    <tr><td style="padding:38px 36px 8px">
      <span style="font:11px Arial,sans-serif;letter-spacing:.22em;color:#9a9a92">PRUEBA DE ARTE</span>
    </td></tr>
    <tr><td style="padding:6px 36px 0;font:20px/1.5 Georgia,serif;color:#222">
      ${primerNombre ? 'Hola ' + html_(primerNombre) + ',' : 'Hola,'}
    </td></tr>
    <tr><td style="padding:10px 36px 0;font:16px/1.65 Georgia,serif;color:#444">
      Ya recorriste las 24 obras y las preguntas. Con lo que elegiste — y, tanto o más,
      con lo que dejaste pasar — esto es lo que apareció:
    </td></tr>
    <tr><td style="padding:26px 36px 0">
      <div style="font:400 36px/1.15 Georgia,serif;color:#171717">${html_(d.profile)}</div>
      ${d.subtitle ? '<div style="font:italic 17px/1.5 Georgia,serif;color:#8a8a84;margin-top:6px">' + html_(d.subtitle) + '</div>' : ''}
    </td></tr>
    ${d.nuances && d.nuances.length ? `<tr><td style="padding:14px 36px 0;font:14px/1.6 Arial,sans-serif;color:#666">
      <b style="color:#333">Con matices de</b> ${html_(d.nuances.join(' · '))}
    </td></tr>` : ''}
    <tr><td style="padding:20px 36px 0;font:16px/1.7 Georgia,serif;color:#333">
      ${html_(d.narrative || '')}
    </td></tr>
    ${d.home_tip ? `<tr><td style="padding:24px 36px 0">
      <p style="font:12px Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8a8a84;margin:0 0 10px">Para tu casa</p>
      <div style="font:15px/1.65 Georgia,serif;color:#444">${html_(d.home_tip)}</div>
    </td></tr>` : ''}
    <tr><td style="padding:6px 36px 0">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="padding:20px 0 0">${bloqueObras_('Tu selección', d.selectionItems, d.selection, baseUrl, 64)}</td></tr>
        <tr><td style="padding:26px 0 0">${bloqueObras_('Para seguir explorando', d.recommendationItems, d.recommendations, baseUrl, 64)}</td></tr>
      </table>
    </td></tr>
    <tr><td style="padding:30px 36px 6px;font:14px/1.6 Arial,sans-serif;color:#555">
      Te dejo también tu resultado en PDF, adjunto a este mail, con más espacio para leerlo
      con calma.
    </td></tr>
    ${d.link ? `<tr><td style="padding:18px 36px 0">
      <a href="${html_(d.link)}" style="display:inline-block;background:#171717;color:#ffffff;
      text-decoration:none;font:14px Arial,sans-serif;padding:13px 22px">Volver a Prueba de Arte</a>
    </td></tr>` : ''}
    <tr><td style="padding:34px 36px 8px">
      <div style="border-top:1px solid #ececE6"></div>
    </td></tr>
    <tr><td style="padding:0 36px 34px;font:italic 14px/1.6 Georgia,serif;color:#8a8a84">
      Tu mirada no es una etiqueta. Es un punto de partida.
    </td></tr>
  </table>
</div>`;
}

// Página del PDF adjunto: mismo resultado, con más espacio, pensado para imprimir o guardar.
function pdfPerfilHtml_(d, nombre) {
  const baseUrl = d.imagesBaseUrl || '';
  const fecha = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'America/Argentina/Buenos_Aires', 'd MMMM yyyy');

  return `<html><head><meta charset="utf-8"></head>
  <body style="font-family:Georgia,'Times New Roman',serif;color:#222;padding:50px 60px;background:#ffffff">
    <p style="font:11px Arial,sans-serif;letter-spacing:.22em;color:#9a9a92;margin:0 0 4px">PRUEBA DE ARTE</p>
    <p style="font:12px Arial,sans-serif;color:#aaaaaa;margin:0 0 40px">${nombre ? html_(nombre) + ' · ' : ''}${fecha}</p>

    <p style="font:400 46px/1.15 Georgia,serif;color:#171717;margin:0">${html_(d.profile)}</p>
    ${d.subtitle ? '<p style="font:italic 20px/1.5 Georgia,serif;color:#8a8a84;margin:10px 0 0">' + html_(d.subtitle) + '</p>' : ''}
    ${d.nuances && d.nuances.length ? '<p style="font:13px Arial,sans-serif;color:#666;margin:18px 0 0"><b style="color:#333">Con matices de</b> ' + html_(d.nuances.join(' · ')) + '</p>' : ''}

    <p style="font:17px/1.75 Georgia,serif;color:#333;margin:26px 0 0;max-width:520px">${html_(d.narrative || '')}</p>
    ${d.home_tip ? '<p style="font:12px Arial,sans-serif;letter-spacing:.14em;color:#8a8a84;margin:30px 0 8px">PARA TU CASA</p>' +
      '<p style="font:15px/1.7 Georgia,serif;color:#444;margin:0;max-width:520px">' + html_(d.home_tip) + '</p>' : ''}

    <div style="margin-top:30px">${bloqueObras_('Tu selección', d.selectionItems, d.selection, baseUrl, 80)}</div>
    <div style="margin-top:26px">${bloqueObras_('Para seguir explorando', d.recommendationItems, d.recommendations, baseUrl, 80)}</div>

    <p style="font:italic 15px/1.6 Georgia,serif;color:#8a8a84;margin:48px 0 0;border-top:1px solid #ececE6;padding-top:20px">
      Tu mirada no es una etiqueta. Es un punto de partida.
    </p>
  </body></html>`;
}

function resumenCasa_(home) {
  const si = home.filter(h => h.answer === 'sí').length;
  return si + ' de ' + home.length + ' sí (' + home.map(h => h.work + ': ' + h.answer).join(' · ') + ')';
}
function textoPruebaPerfil_(pt) {
  return (TEXTO_PRUEBA_PERFIL[pt.chose] || pt.chose) + ' (suyo ' + pt.own + ' vs ' + pt.other + ')';
}

// ---------- utilidades de planilla ----------
function buscarFila_(sh, id) {
  const last = sh.getLastRow();
  if (last < 2) return 0;
  const hit = sh.getRange(2, 1, last - 1, 1).createTextFinder(id).matchEntireCell(true).findNext();
  return hit ? hit.getRow() : 0;
}
function leerFila_(sh, fila) {
  const vals = sh.getRange(fila, 1, 1, COLS_SESIONES.length).getValues()[0];
  const o = {};
  COLS_SESIONES.forEach((c, i) => { o[c] = vals[i]; });
  return o;
}
function escribirFila_(sh, fila, o) {
  const row = COLS_SESIONES.map(c => (o[c] === undefined || o[c] === null) ? '' : o[c]);
  if (fila) sh.getRange(fila, 1, 1, row.length).setValues([row]);
  else sh.appendRow(row);
}
function recortar_(x, n) { return x == null ? '' : String(x).slice(0, n); }
function html_(x) {
  return String(x == null ? '' : x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
