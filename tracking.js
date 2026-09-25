// Envío de datos a la planilla de Google (Apps Script).
// Cada evento viaja como texto JSON; "no-cors" evita problemas de permisos entre dominios.
// Las pruebas hechas desde tu PC (localhost) o con ?test=1 en el link quedan marcadas como prueba.
const Tracking = (() => {
  const cfg = window.PRUEBA_CONFIG || {};
  const isTest = /[?&]test=1\b/.test(location.search) ||
    ['localhost', '127.0.0.1', ''].includes(location.hostname);
  const newId = () => (window.crypto && crypto.randomUUID)
    ? crypto.randomUUID()
    : Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  let sid = newId();

  function device() {
    return {
      mobile: window.matchMedia('(max-width: 700px)').matches,
      width: window.innerWidth,
      height: window.innerHeight,
      lang: navigator.language || '',
      ua: (navigator.userAgent || '').slice(0, 180)
    };
  }

  function send(type, data = {}) {
    const payload = { v: 1, session_id: sid, type, test: isTest, ts: new Date().toISOString(), ...data };
    if (!cfg.webhookUrl) { console.info('[Prueba de Arte · sin URL configurada]', payload); return; }
    try {
      fetch(cfg.webhookUrl, {
        method: 'POST', mode: 'no-cors', keepalive: true,
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify(payload)
      }).catch(() => {});
    } catch (e) { /* nunca romper la experiencia por un error de envío */ }
  }

  return {
    send, device,
    newSession() { sid = newId(); },
    // Al retomar un recorrido guardado, seguimos usando la misma sesión (misma fila en la planilla).
    setSession(id) { if (typeof id === 'string' && id && id.length <= 64) sid = id; },
    get sessionId() { return sid; },
    get isTest() { return isTest; },
    get enabled() { return !!cfg.webhookUrl; }
  };
})();
