# QA checklist — Prueba de Arte

## Carga
- [x] `index.html` carga desde servidor local.
- [x] Los 5 JSON se cargan sin error.
- [x] 60 obras presentes.
- [x] 24 duelos presentes.
- [x] 10 perfiles presentes.
- [x] 7 preguntas presentes.
- [x] 8 ejes presentes.

## Recorrido
- [x] Intro → identidad → primer duelo.
- [x] 24 decisiones.
- [x] Primeros 16 duelos fijos.
- [x] Últimos 8 duelos adaptativos.
- [x] A / B / Ambas / Ninguna.
- [x] Pausa cada 4 duelos.
- [x] Preguntas Q01–Q06 en sus puntos previstos, incluida Q06 después del duelo 22.
- [x] Q07 aparece después del duelo 24 y antes del resultado.
- [x] Q07 usa la última obra elegida directamente cuando existe.
- [x] No hay navegación hacia atrás.

## Resultado
- [x] Perfil principal + matices.
- [x] 5 ejes visuales destacados.
- [x] Mi selección con diversidad de familias/artistas.
- [x] Recomendaciones nuevas.
- [x] Evitación de obras rechazadas.
- [x] Ruta de exploración de 5 pasos.
- [x] Reflexión final opcional.
- [x] Pared visual.
- [x] Impresión / PDF mediante diálogo del navegador.

## Robustez
- [x] Fallback si una imagen remota falla.
- [x] HTML escapado para textos dinámicos.
- [x] `node --check app.js` OK.
- [x] `validate.py` OK.
- [ ] Validación individual de las 60 URLs de imagen desde el hosting definitivo.
- [ ] Descarga local y validación de las 60 imágenes (`tools/fetch_images.py` + `tools/validate_images.py`).
- [ ] Prueba F&F con usuarios reales.
