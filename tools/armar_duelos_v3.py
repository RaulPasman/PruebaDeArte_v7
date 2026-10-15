#!/usr/bin/env python3
"""Arma data/v3/duels.json: banco de ~270 duelos para el test de 60 (curaduría 3.0).

Cómo se usa el banco en la app (app.js, modo v3): a cada persona se le sortean 36 duelos del banco
sin repetir ninguna obra (cada uno ve combinaciones distintas), y los 24 restantes son adaptativos
(se eligen del resto del banco los que mejor separan sus dos perfiles candidatos).

Reglas de cada duelo (las mismas del test anterior):
- nunca dos obras de la misma familia ni del mismo artista;
- fama parecida (diferencia máxima 1), para que no gane "la que conozco";
- mucho contraste entre las dos obras, repartido entre los 8 ejes;
- cada obra aparece en 3 duelos (así todas se ven y ninguna domina).

Uso: python tools/armar_duelos_v3.py            (muestra el resumen)
     python tools/armar_duelos_v3.py --escribir  (guarda data/v3/duels.json)
"""
import json, math, random, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = json.loads((ROOT / "data" / "v3" / "artworks.json").read_text(encoding="utf-8"))
AX = [k for k in A[0] if k[:1] == "E" and k[1].isdigit()]
W = {w["ID"]: w for w in A}
IDS = sorted(W)
V = {i: [W[i][a] for a in AX] for i in IDS}
DEG = 3  # duelos por obra


def ok(a, b):
    wa, wb = W[a], W[b]
    return (wa["Familia"] != wb["Familia"] and wa["Artista"] != wb["Artista"]
            and abs(wa.get("Fama", 1) - wb.get("Fama", 1)) <= 1)


def contrast(a, b):
    d = [abs(x - y) for x, y in zip(V[a], V[b])]
    # contraste total, pero premiando que esté repartido (raíz por eje) y no sólo en un eje
    return sum(math.sqrt(x) for x in d)


def build(seed):
    rnd = random.Random(seed)
    pairs = [(a, b) for i, a in enumerate(IDS) for b in IDS[i + 1:] if ok(a, b)]
    scored = sorted(pairs, key=lambda p: -(contrast(*p) + rnd.uniform(0, 0.8)))
    deg, used, out = Counter(), set(), []
    for a, b in scored:  # pasada 1: los de más contraste, sin pasarse de DEG por obra
        if deg[a] < DEG and deg[b] < DEG:
            out.append((a, b)); deg[a] += 1; deg[b] += 1; used.add((a, b))
    for a in IDS:  # pasada 2: completar obras con pocos duelos
        while deg[a] < DEG:
            cand = [b for b in IDS if b != a and ok(a, b) and deg[b] < DEG + 1 and (min(a, b), max(a, b)) not in used]
            if not cand: break
            b = max(cand, key=lambda b: contrast(a, b) - 0.6 * deg[b])
            p = (min(a, b), max(a, b))
            out.append(p); used.add(p); deg[a] += 1; deg[b] += 1
    return out, deg


def main():
    best = None
    for seed in range(20):
        out, deg = build(seed)
        worst = min(contrast(a, b) for a, b in out)
        score = sum(contrast(a, b) for a, b in out) / len(out) + 0.5 * worst
        if best is None or score > best[0]:
            best = (score, out, deg)
    _, out, deg = best
    rnd = random.Random(7)
    rnd.shuffle(out)
    duels = []
    for k, (a, b) in enumerate(out, 1):
        if rnd.random() < 0.5: a, b = b, a  # lado izquierdo/derecho al azar
        duels.append({"id": f"B{k:03d}", "a": a, "b": b, "contrast": round(contrast(a, b), 2)})
    cs = [d["contrast"] for d in duels]
    fam = Counter(f"{W[d['a']]['Familia'][:12]} / {W[d['b']]['Familia'][:12]}" for d in duels)
    print(f"{len(duels)} duelos; obras con su cantidad de duelos: {dict(Counter(deg.values()))}")
    print(f"contraste: mín {min(cs):.2f} · promedio {sum(cs)/len(cs):.2f} · máx {max(cs):.2f}")
    print(f"duelos conocida vs conocida: {sum(1 for d in duels if W[d['a']]['Tier']==W[d['b']]['Tier']=='Conocida')}, "
          f"poco conocida vs poco conocida: {sum(1 for d in duels if W[d['a']]['Tier']==W[d['b']]['Tier']=='Poco conocida')}")
    if "--escribir" in sys.argv:
        (ROOT / "data" / "v3" / "duels.json").write_text(json.dumps(duels, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print("guardado data/v3/duels.json")


if __name__ == "__main__":
    main()
