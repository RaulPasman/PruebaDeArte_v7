#!/usr/bin/env python3
"""Arma data/duels.json: 16 duelos fijos (D01–D16) + banco adaptativo de 16 (D17–D32).

Reglas de cada duelo:
- nunca dos obras de la misma familia;
- fama parecida (diferencia máxima 1 en la escala 1–3 del campo "Fama"), para que no gane "la que conozco";
- mucho contraste entre las dos obras, repartido entre los 8 ejes (no sólo abstracto vs figurativo);
- al menos 6 duelos entre dos abstracciones de distinto tipo, en los fijos y en el banco, porque el
  público es mayormente abstracto y hay que distinguir *qué* abstracción prefiere.

Uso: python tools/armar_duelos.py            (muestra la propuesta)
     python tools/armar_duelos.py --escribir  (la guarda en data/duels.json)
"""
import json, math, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = json.loads((ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))
AX = [k for k in A[0] if k[:1] == "E" and k[1].isdigit()]
W = {w["ID"]: w for w in A}
IDS = sorted(W)
V = {i: [W[i][a] for a in AX] for i in IDS}
ABS = {i for i in IDS if W[i][AX[0]] <= -0.3}


def ok(a, b):
    return W[a]["Familia"] != W[b]["Familia"] and abs(W[a].get("Fama", 1) - W[b].get("Fama", 1)) <= 1


def diff(a, b):
    return [abs(x - y) for x, y in zip(V[a], V[b])]


def score(pairs, min_abs):
    cov = [0.0] * len(AX)
    for a, b in pairs:
        for k, d in enumerate(diff(a, b)):
            cov[k] += d
    worst = min(sum(diff(a, b)) for a, b in pairs)
    n_abs = sum(1 for a, b in pairs if a in ABS and b in ABS)
    return sum(math.sqrt(c) for c in cov) + 0.6 * worst - 3.0 * max(0, min_abs - n_abs)


def optimize(pool, n_pairs, min_abs, seed, iters=60000):
    rnd = random.Random(seed)
    best = None
    for restart in range(12):
        items = pool[:]
        rnd.shuffle(items)
        pairs = []
        used = set()
        for a in items:
            if a in used: continue
            cand = [b for b in items if b not in used and b != a and ok(a, b)]
            if not cand: continue
            b = max(cand, key=lambda b: sum(diff(a, b)) + rnd.random())
            pairs.append((a, b)); used |= {a, b}
            if len(pairs) == n_pairs: break
        if len(pairs) < n_pairs: continue
        cur = score(pairs, min_abs)
        free = [i for i in pool if i not in {x for p in pairs for x in p}]
        for _ in range(iters):
            i = rnd.randrange(n_pairs)
            a, b = pairs[i]
            move = rnd.random()
            new = pairs[:]
            if move < 0.5 and free:          # cambiar una obra por una que no se usa
                k = rnd.randrange(len(free)); x = free[k]
                na, nb = (x, b) if rnd.random() < 0.5 else (a, x)
                if not ok(na, nb): continue
                new[i] = (na, nb)
                s = score(new, min_abs)
                if s >= cur:
                    out = a if na == x else b
                    free[k] = out; pairs, cur = new, s
            else:                             # intercambiar parejas entre dos duelos
                j = rnd.randrange(n_pairs)
                if i == j: continue
                c, d = pairs[j]
                if not (ok(a, d) and ok(c, b)): continue
                new[i], new[j] = (a, d), (c, b)
                s = score(new, min_abs)
                if s >= cur: pairs, cur = new, s
        if best is None or cur > best[0]:
            best = (cur, pairs)
    return best


def label(i):
    w = W[i]
    return f"{i} {w['Artista']} (fama {w.get('Fama', 1)})"


def main():
    fixed_score, fixed = optimize(IDS, 16, 6, seed=1)
    used = {x for p in fixed for x in p}
    rest = [i for i in IDS if i not in used]
    bank_score, bank = optimize(rest, 14, 5, seed=2)
    used_bank = {x for p in bank for x in p}
    # 2 duelos extra del banco con obras que no aparecen en ningún otro lado + máximo contraste
    left = [i for i in IDS if i not in used and i not in used_bank]
    extras = []
    pool = left + rest
    for _ in range(2):
        cands = [(a, b) for a in pool for b in pool if a < b and ok(a, b)
                 and (a, b) not in bank + extras and (b, a) not in bank + extras
                 and (a in left or b in left or not left)]
        best = max(cands, key=lambda p: sum(diff(*p)) + (5 if (p[0] in left or p[1] in left) else 0))
        extras.append(best)
        left = [i for i in left if i not in best]
    bank += extras
    duels = []
    for n, (a, b) in enumerate(fixed + bank, 1):
        if random.Random(n).random() < 0.5: a, b = b, a      # A/B al azar
        fa, fb = W[a]["Familia"].split(" /")[0].split(":")[0].lower(), W[b]["Familia"].split(" /")[0].split(":")[0].lower()
        duels.append({"id": f"D{n:02}", "a": a, "b": b, "rationale": f"{fa} vs {fb}"})
    for d in duels:
        tag = "fijo " if int(d["id"][1:]) <= 16 else "banco"
        both = "  [abstracto vs abstracto]" if d["a"] in ABS and d["b"] in ABS else ""
        print(f"{d['id']} {tag} {sum(diff(d['a'], d['b'])):.1f}  {label(d['a'])}  vs  {label(d['b'])}{both}")
    never = [i for i in IDS if not any(i in (d["a"], d["b"]) for d in duels)]
    print("Obras sin duelo:", never or "ninguna")
    if "--escribir" in sys.argv:
        (ROOT / "data" / "duels.json").write_text(json.dumps(duels, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
        print("Guardado en data/duels.json")


if __name__ == "__main__":
    main()
