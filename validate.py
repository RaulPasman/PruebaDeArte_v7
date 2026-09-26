#!/usr/bin/env python3
"""Chequeo de datos de Prueba de Arte. Uso: python validate.py

No exige cantidades fijas (se puede crecer a más obras o duelos): controla que todo sea
coherente. ERROR = hay que arreglarlo antes de publicar. AVISO = conviene revisarlo.
"""
import json, sys
from collections import Counter
from pathlib import Path

root = Path(__file__).parent
load = lambda name: json.loads((root / "data" / name).read_text(encoding="utf-8"))
A, D, P, Q, S = (load(f) for f in ("artworks.json", "duels.json", "profiles.json", "questions.json", "scoring.json"))
AXES = ["E1 Abstracto↔Figurativo", "E2 Estructurado↔Espontáneo", "E3 Sereno↔Expresivo",
        "E4 Contenido↔Saturado", "E5 Plano↔Material", "E6 Cotidiano↔Imaginario",
        "E7 Íntimo↔Dominante", "E8 Transparente↔Conceptual"]
FIXED_DUELS, TOTAL_DUELS = 16, 24  # app.js: los primeros 16 duelos son fijos, el resto adaptativos
errors, warns = [], []

ids = [w["ID"] for w in A]
for i, n in Counter(ids).items():
    if n > 1: errors.append(f"obra {i} repetida {n} veces")
ids = set(ids)
for w in A:
    for ax in AXES:
        v = w.get(ax)
        if not isinstance(v, (int, float)) or not -1 <= v <= 1:
            errors.append(f"{w['ID']}: eje '{ax}' inválido ({v})")
    for k in ("Título", "Artista", "Familia", "image_file"):
        if not w.get(k): errors.append(f"{w['ID']}: falta '{k}'")
    if w.get("image_file") and not (root / w["image_file"]).is_file():
        errors.append(f"{w['ID']}: no existe la imagen {w['image_file']}")
for (t, a), n in Counter((w["Título"].strip().lower(), w["Artista"].strip().lower()) for w in A).items():
    if n > 1:
        warns.append(f"la misma obra aparece {n} veces: {t} ({a}) -> " +
                     ", ".join(w["ID"] for w in A if w["Título"].strip().lower() == t and w["Artista"].strip().lower() == a))

dids = [d["id"] for d in D]
for i, n in Counter(dids).items():
    if n > 1: errors.append(f"duelo {i} repetido")
if len(D) < TOTAL_DUELS:
    errors.append(f"hay {len(D)} duelos; hacen falta al menos {TOTAL_DUELS} ({FIXED_DUELS} fijos + banco adaptativo)")
for d in D:
    if d["a"] not in ids or d["b"] not in ids: errors.append(f"duelo {d['id']}: usa una obra que no existe")
    if d["a"] == d["b"]: errors.append(f"duelo {d['id']}: enfrenta una obra consigo misma")
in_duels = {x for d in D for x in (d["a"], d["b"])}
never = sorted(ids - in_duels)
if never:
    warns.append(f"{len(never)} obras nunca aparecen en un duelo: {', '.join(never)}")

for p in P:
    if set(p["vector"]) != set(AXES): errors.append(f"perfil {p['id']}: ejes incompletos")
    if not all(-1 <= v <= 1 for v in p["vector"].values()): errors.append(f"perfil {p['id']}: valor fuera de rango")
if not any(p["id"] == "P10" for p in P): errors.append("falta el perfil P10 (explorador sin fronteras, se usa de respaldo)")

for q in Q:
    if not 1 <= q["afterDuel"] <= TOTAL_DUELS: errors.append(f"pregunta {q['id']}: afterDuel fuera de rango")
    for o in q["options"]:
        for k, v in o.get("signals", {}).items():
            if not any(ax.startswith(k + " ") for ax in AXES): errors.append(f"pregunta {q['id']}: eje desconocido {k}")
            if not -1 <= v <= 1: errors.append(f"pregunta {q['id']}: señal fuera de rango")
if not any(q["id"] == "Q07" for q in Q): errors.append("falta la pregunta Q07 (la última, con obra)")

for k in ("direct", "both", "neither", "question_default", "question_multiplier"):
    if not isinstance(S.get("weights", {}).get(k), (int, float)): errors.append(f"scoring.json: falta weights.{k}")
if len(S.get("duel_phase_weights", [])) != 3 or len(S.get("duel_phase_breaks", [])) != 2:
    errors.append("scoring.json: duel_phase_weights necesita 3 valores y duel_phase_breaks 2")

for w in warns: print("AVISO:", w)
for e in errors: print("ERROR:", e)
fams = len({w["Familia"] for w in A})
print(f"\n{len(A)} obras · {fams} familias · {len(D)} duelos · {len(P)} perfiles · {len(Q)} preguntas")
print("OK" if not errors else f"{len(errors)} errores")
sys.exit(1 if errors else 0)
