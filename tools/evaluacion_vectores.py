#!/usr/bin/env python3
"""Doble evaluación de los vectores de las obras (Revisión Integral, sección 3).

1) python tools/evaluacion_vectores.py plantilla
   Crea docs/evaluacion/plantilla_vectores.csv: una fila por obra, con los 8 ejes vacíos.
   Cada evaluador (Raúl y alguien del mundo del arte) completa SU copia por separado, sin ver
   los valores actuales ni los del otro. Se abre con Excel o Google Sheets; separador ';'.
   Valores de -1 a 1 (se acepta coma o punto decimal: -0,5 o -0.5).

2) python tools/evaluacion_vectores.py comparar evaluador1.csv evaluador2.csv
   Lista las obras y ejes donde los dos evaluadores difieren en más de 0,5, y crea
   docs/evaluacion/propuesta_vectores.csv con el promedio de ambos, para revisar antes de
   cargarlo en data/artworks.json (y correr el simulador antes y después).
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "evaluacion"
AXES = ["E1 Abstracto↔Figurativo", "E2 Estructurado↔Espontáneo", "E3 Sereno↔Expresivo",
        "E4 Contenido↔Saturado", "E5 Plano↔Material", "E6 Cotidiano↔Imaginario",
        "E7 Íntimo↔Dominante", "E8 Transparente↔Conceptual"]
HEAD = ["ID", "Obra", "Artista"] + AXES
LIMITE = 0.5


def obras():
    works = json.loads((ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))
    return [(w["ID"], w["Título"], w["Artista"]) for w in works]


def plantilla():
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "plantilla_vectores.csv"
    with f.open("w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.writer(fh, delimiter=";")
        wr.writerow(HEAD)
        for row in obras():
            wr.writerow(list(row) + [""] * len(AXES))
    print(f"Listo: {f.relative_to(ROOT)} ({len(obras())} obras)")


def leer(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    head, data = rows[0], rows[1:]
    idx = {ax: head.index(ax) for ax in AXES}
    out = {}
    for r in data:
        if not r or not r[0].strip():
            continue
        vals = {}
        for ax in AXES:
            txt = r[idx[ax]].strip().replace(",", ".") if idx[ax] < len(r) else ""
            vals[ax] = float(txt) if txt else None
        out[r[0].strip()] = (r[1], r[2], vals)
    return out


def comparar(a_path, b_path):
    a, b = leer(a_path), leer(b_path)
    desacuerdos, faltan, prom = [], [], []
    for code in sorted(set(a) | set(b)):
        if code not in a or code not in b:
            faltan.append(code); continue
        obra, artista, va = a[code]
        vb = b[code][2]
        fila = [code, obra, artista]
        for ax in AXES:
            x, y = va[ax], vb[ax]
            if x is None or y is None:
                faltan.append(f"{code} {ax[:2]}"); fila.append(""); continue
            if abs(x - y) > LIMITE:
                desacuerdos.append(f"{code} {artista} — {ax}: {x:+.1f} vs {y:+.1f}")
            fila.append(f"{(x + y) / 2:.2f}".replace(".", ","))
        prom.append(fila)
    print(f"Desacuerdos de más de {LIMITE} ({len(desacuerdos)}):")
    for d in desacuerdos:
        print("  " + d)
    if faltan:
        print(f"Sin completar en alguno de los dos: {', '.join(faltan)}")
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "propuesta_vectores.csv"
    with f.open("w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.writer(fh, delimiter=";")
        wr.writerow(HEAD)
        wr.writerows(prom)
    print(f"\nPromedio guardado en {f.relative_to(ROOT)}. Discutan los desacuerdos antes de usarlo.")


if __name__ == "__main__":
    if sys.argv[1:2] == ["plantilla"]:
        plantilla()
    elif sys.argv[1:2] == ["comparar"] and len(sys.argv) == 4:
        comparar(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
