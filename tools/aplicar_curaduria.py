#!/usr/bin/env python3
"""Aplica reemplazos de la curaduría 1.1 (data/curaduria_1_1.json) a data/artworks.json.

Uso:  python tools/aplicar_curaduria.py --ids B06,C04
      python tools/aplicar_curaduria.py --listar

Cada obra reemplazada conserva su ID (así los duelos siguen funcionando). Para aplicar una obra
tiene que tener título y año definidos y, si no se baja sola de Wikipedia/Commons, su imagen ya
guardada en assets/manual/ID.jpg. Después de aplicar:
  1) python tools/fetch_images.py --only IDS --force   (procesa la imagen nueva)
  2) abrir REVISAR_IMAGENES.html y confirmar que cada imagen es la obra nueva
  3) correr SIMULADOR_MOTOR.html y comparar con los números de CLAUDE.md
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTWORKS = ROOT / "data" / "artworks.json"
SOURCES = ROOT / "data" / "image_sources.json"
CURA = ROOT / "data" / "curaduria_1_1.json"
MANUAL = ROOT / "assets" / "manual"
AXES = ["E1 Abstracto↔Figurativo", "E2 Estructurado↔Espontáneo", "E3 Sereno↔Expresivo",
        "E4 Contenido↔Saturado", "E5 Plano↔Material", "E6 Cotidiano↔Imaginario",
        "E7 Íntimo↔Dominante", "E8 Transparente↔Conceptual"]


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, data):
    # Respeta la sangría y el salto final que ya tenía cada archivo, para que el cambio sea mínimo.
    old = p.read_text(encoding="utf-8")
    indent = 1 if old.startswith("{\n \"") or old.startswith("[\n {") else 2
    text = json.dumps(data, ensure_ascii=False, indent=indent) + ("\n" if old.endswith("\n") else "")
    p.write_text(text, encoding="utf-8", newline="\n")


def manual_image(code):
    return next((f for f in MANUAL.glob(f"{code}*") if f.is_file() and f.name != ".gitkeep"), None)


def problems(code, e):
    out = []
    if not e.get("Título"):
        out.append("falta elegir la obra puntual (Título vacío)")
    if not e.get("Año"):
        out.append("falta el año")
    if len(e.get("vector", [])) != 8 or not all(-1 <= v <= 1 for v in e["vector"]):
        out.append("el vector tiene que tener 8 valores entre -1 y 1")
    src = e.get("image_source") or {}
    if not (src.get("wiki") or src.get("commons_file")) and not manual_image(code):
        out.append(f"falta la imagen: guardala como assets/manual/{code}.jpg")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="", help="IDs separados por coma, ej: B06,C04")
    ap.add_argument("--listar", action="store_true", help="mostrar el estado de cada reemplazo")
    args = ap.parse_args()
    cura = load(CURA)
    entries = {k: v for k, v in cura.items() if not k.startswith("_")}

    if args.listar or not args.ids:
        for code, e in entries.items():
            pend = problems(code, e) if e["estado"] != "aplicada" else []
            estado = e["estado"] if not pend else "pendiente: " + "; ".join(pend)
            print(f"{code}  {e['Artista']:<22} {estado}")
        return 0

    ids = [x.strip().upper() for x in args.ids.split(",") if x.strip()]
    works = load(ARTWORKS)
    sources = load(SOURCES)
    by_id = {w["ID"]: w for w in works}
    bad = False
    for code in ids:
        e = entries.get(code)
        if not e:
            print(f"{code}: no está en data/curaduria_1_1.json"); bad = True; continue
        if code not in by_id:
            print(f"{code}: no existe en data/artworks.json"); bad = True; continue
        pend = problems(code, e)
        if pend:
            print(f"{code}: no se aplica — " + "; ".join(pend)); bad = True; continue
        w = by_id[code]
        for k in ("Título", "Artista", "Año", "Medio", "Familia", "Fuente/licencia", "context"):
            w[k] = e[k]
        for ax, v in zip(AXES, e["vector"]):
            w[ax] = v
        src = e.get("image_source") or {}
        manual = not (src.get("wiki") or src.get("commons_file"))
        w["image_source"] = "Manual (assets/manual)" if manual else "Wikipedia / Wikimedia Commons"
        w["image_status"] = "CANDIDATE"
        w["image_url"] = e.get("image_url", "")
        w["image_file"] = f"assets/artworks/{code}.jpg"
        sources[code] = src if not manual else {
            "wiki": [], "nota": f"Curaduría 1.1: imagen manual en assets/manual/{code}.jpg"}
        e["estado"] = "aplicada"
        print(f"{code}: aplicada — {e['Artista']}, {e['Título']} ({e['Año']})")

    save(ARTWORKS, works)
    save(SOURCES, sources)
    save(CURA, cura)
    print(f"\nAhora: python tools/fetch_images.py --only {','.join(ids)} --force")
    print("y revisá REVISAR_IMAGENES.html: tiene que verse la obra NUEVA en cada ID.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
