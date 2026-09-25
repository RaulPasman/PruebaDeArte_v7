#!/usr/bin/env python3
"""Prueba de Arte — descargador de imágenes v7.

Por qué falló la v6
-------------------
1. Wikimedia ahora rechaza (HTTP 429) miniaturas en tamaños no estándar. La v6
   pedía 2400 px; los tamaños válidos son 20/40/60/120/250/330/500/960/1280/1920/3840.
2. Hacía ~5 búsquedas por obra (~300 llamadas) con un User-Agent genérico y sin
   esperar ante un 429. Wikimedia lo trató como bot abusivo y cortó todo.
3. Buscaba en Commons por texto libre. Commons NO aloja obras con derechos
   vigentes (Pollock, Matisse, Dalí, Magritte, Warhol, Kahlo...), así que esas
   búsquedas nunca iban a encontrar la obra, y otras devolvían archivos
   equivocados (detalles, fotos de sala, recortes).

Qué hace la v7
--------------
1. Usa la imagen principal del artículo de Wikipedia de cada obra (elegida por
   editores: es la obra completa, no un detalle). Funciona también para obras
   con derechos, que Wikipedia muestra en baja resolución.
2. Resuelve las 60 obras en pocas llamadas agrupadas (hasta 50 títulos por llamada).
3. Pide miniaturas de 1920 px (tamaño estándar) y respeta Retry-After con
   reintentos progresivos.
4. Es reanudable: si se corta, volvés a ejecutarlo y sigue donde quedó.
5. No modifica data/artworks.json. Deja un registro en data/image_manifest.json
   y una hoja de control visual en REVISAR_IMAGENES.html.
6. Si una imagen no te convence, poné tu propio archivo en assets/manual/ID.jpg
   (por ejemplo assets/manual/C04.jpg) y volvé a ejecutar: ése gana siempre.

Uso:
    py tools/fetch_images.py                  # descarga lo que falta
    py tools/fetch_images.py --only C04,G02   # sólo esas obras
    py tools/fetch_images.py --force          # rehace todo
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import unicodedata
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    print("ERROR: falta Pillow. Ejecutá:  py -m pip install pillow")
    raise SystemExit(3)

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
# Wikimedia pide un User-Agent que identifique el proyecto y un contacto.
# Reemplazá el mail por el tuyo (o definí la variable de entorno PRUEBA_CONTACTO).
CONTACTO = os.environ.get("PRUEBA_CONTACTO", "testdearteraulpasman@gmail.com")
UA = (f"PruebaDeArte-ImageFetcher/0.7.1 (prototipo privado F&F; {CONTACTO}) "
      f"Python-urllib/{sys.version_info[0]}.{sys.version_info[1]}")

ROOT = Path(__file__).resolve().parents[1]
ARTWORKS = ROOT / "data" / "artworks.json"
SOURCES = ROOT / "data" / "image_sources.json"
MANIFEST = ROOT / "data" / "image_manifest.json"
OUT = ROOT / "assets" / "artworks"
MANUAL = ROOT / "assets" / "manual"
REVIEW = ROOT / "REVISAR_IMAGENES.html"

WP_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
THUMB_STEP = 1920          # tamaño estándar de Wikimedia (no usar valores arbitrarios)
WEB_MAX_PX = 1600          # tamaño final para la web (sobra para duelos en pantallas retina)
LOW_RES_PX = 700           # por debajo de esto se marca como baja resolución
PAUSE_API = 1.0            # segundos entre llamadas a la API
PAUSE_DOWNLOAD = 1.5       # segundos entre descargas
MAX_RETRIES = 6

STOP = {"the", "a", "an", "and", "of", "in", "on", "with", "from", "for", "to", "at", "by",
        "no", "oil", "canvas", "painting", "la", "le", "de", "des", "du", "el", "untitled"}


# ---------------------------------------------------------------------------
# HTTP con reintentos
# ---------------------------------------------------------------------------
class Http:
    """Encapsula la red (se puede reemplazar en tests)."""

    def __init__(self, verbose: bool = True, sleep=time.sleep):
        self.verbose = verbose
        self.calls = 0
        self.sleep = sleep

    def _open(self, url: str, accept: str, timeout: int) -> bytes:
        req = Request(url, headers={"User-Agent": UA, "Accept": accept})
        with urlopen(req, timeout=timeout) as r:
            return r.read()

    def get(self, url: str, accept: str = "application/json", timeout: int = 40) -> bytes:
        wait = 5.0
        for attempt in range(1, MAX_RETRIES + 1):
            self.calls += 1
            try:
                return self._open(url, accept, timeout)
            except HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                    ra = e.headers.get("Retry-After") if e.headers else None
                    delay = float(ra) if ra and str(ra).isdigit() else wait
                    delay = min(delay, 180)
                    if self.verbose:
                        print(f"      Wikimedia pidió esperar (HTTP {e.code}). "
                              f"Reintento {attempt}/{MAX_RETRIES - 1} en {delay:.0f}s...")
                    self.sleep(delay)
                    wait = min(wait * 2.5, 180)
                    continue
                raise
            except (URLError, TimeoutError) as e:
                if attempt < MAX_RETRIES:
                    if self.verbose:
                        print(f"      Problema de red ({e}). Reintento en {wait:.0f}s...")
                    self.sleep(wait)
                    wait = min(wait * 2.5, 180)
                    continue
                raise
        raise RuntimeError("sin respuesta tras varios reintentos")

    def api(self, base: str, params: dict) -> dict:
        params = {**params, "format": "json", "formatversion": 2, "maxlag": 5}
        data = json.loads(self.get(f"{base}?{urlencode(params)}").decode("utf-8"))
        self.sleep(PAUSE_API)
        if "error" in data:
            raise RuntimeError(f"API: {data['error'].get('info', data['error'])}")
        return data


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def tokens(s: str) -> set:
    return {t for t in norm(s).split() if t not in STOP and len(t) > 1}


def chunks(seq, n=50):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def follow_titles(query: dict):
    """Devuelve una función título pedido -> título final (normalización + redirección)."""
    m = {}
    for key in ("normalized", "redirects"):
        for x in query.get(key, []) or []:
            m[x["from"]] = x["to"]

    def final(t):
        seen = set()
        while t in m and t not in seen:
            seen.add(t)
            t = m[t]
        return t
    return final


# ---------------------------------------------------------------------------
# Resolución: obra -> archivo de imagen
# ---------------------------------------------------------------------------
def page_images(http: Http, titles: list) -> dict:
    """{título pedido: nombre de archivo de la imagen principal del artículo, o None}."""
    out = {}
    for group in chunks(sorted(set(titles))):
        data = http.api(WP_API, {"action": "query", "prop": "pageimages", "piprop": "name", "pilicense": "any",
                                 "titles": "|".join(group), "redirects": 1})
        q = data.get("query", {})
        final = follow_titles(q)
        by_title = {p.get("title"): p for p in q.get("pages", [])}
        for t in group:
            p = by_title.get(final(t))
            out[t] = p.get("pageimage") if p and not p.get("missing") else None
    return out


def wiki_search(http: Http, query: str, work: dict) -> list:
    data = http.api(WP_API, {"action": "query", "list": "search", "srsearch": query,
                             "srnamespace": 0, "srlimit": 5})
    artist_norm = norm(work["Artista"])
    title_tok = tokens(work["Título"])
    ranked = []
    for r in data.get("query", {}).get("search", []):
        t = r.get("title", "")
        if norm(t) == artist_norm:   # artículo del artista -> daría su retrato, no la obra
            continue
        overlap = len(title_tok & tokens(t))
        if overlap:
            ranked.append((overlap, t))
    ranked.sort(key=lambda x: -x[0])
    return [t for _, t in ranked[:2]]


def commons_search(http: Http, query: str, work: dict):
    """Último recurso: sólo sirve para obras de dominio público sin artículo propio."""
    data = http.api(COMMONS_API, {"action": "query", "list": "search", "srsearch": query,
                                  "srnamespace": 6, "srlimit": 10})
    title_tok = tokens(work["Título"])
    surname = norm(work["Artista"]).split()[-1] if norm(work["Artista"]) else ""
    best, best_score = None, 0
    for r in data.get("query", {}).get("search", []):
        t = r.get("title", "")
        nt = norm(t)
        if any(b in nt.split() for b in ("detail", "detalle", "cropped", "signature", "frame", "label")):
            continue
        score = 3 * len(title_tok & set(nt.split())) + (5 if surname and surname in nt else 0)
        if score > best_score:
            best, best_score = t, score
    need = 5 + 3 * min(2, len(title_tok))
    return best.split(":", 1)[1] if best and best_score >= need else None


def image_info(http: Http, files: list) -> dict:
    """{archivo: {url, width, height, repo}} usando miniaturas de tamaño estándar."""
    out = {}
    for group in chunks(sorted(set(files))):
        titles = [f"File:{f}" for f in group]
        data = http.api(WP_API, {"action": "query", "prop": "imageinfo", "titles": "|".join(titles),
                                 "iiprop": "url|size|mime|thumbmime", "iiurlwidth": THUMB_STEP})
        q = data.get("query", {})
        final = follow_titles(q)
        by_title = {p.get("title"): p for p in q.get("pages", [])}
        for f, t in zip(group, titles):
            p = by_title.get(final(t)) or {}
            info = (p.get("imageinfo") or [{}])[0]
            url = info.get("thumburl") or info.get("url")
            mime = info.get("thumbmime") or info.get("mime") or ""
            if not url or not mime.startswith("image/"):
                continue
            out[f] = {
                "url": url,
                "page": info.get("descriptionurl"),
                "width": info.get("thumbwidth") or info.get("width") or 0,
                "height": info.get("thumbheight") or info.get("height") or 0,
                "repo": ("commons" if "/wikipedia/commons/" in (info.get("url") or "")
                         else "wikipedia-en (uso limitado)"),
            }
    return out


# ---------------------------------------------------------------------------
# Archivos locales
# ---------------------------------------------------------------------------
def save_web_jpg(src, dest: Path) -> tuple:
    src = BytesIO(src) if isinstance(src, (bytes, bytearray)) else src
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((WEB_MAX_PX, WEB_MAX_PX), Image.Resampling.LANCZOS)
        tmp = dest.with_suffix(".tmp")
        im.save(tmp, "JPEG", quality=85, optimize=True, progressive=True)
        tmp.replace(dest)
        return im.size


def valid_local(p: Path) -> bool:
    try:
        if not p.exists() or p.stat().st_size < 1500:
            return False
        with Image.open(p) as im:
            im.verify()
        return True
    except Exception:
        return False


def manual_file(code: str):
    """Busca en assets/manual/ cualquier archivo que empiece con el ID de la obra,
    sin importar mayúsculas ni la extensión que tenga (incluidas extensiones dobles
    como "C04.jpg.jfif", típicas cuando Windows oculta la extensión real al renombrar
    un archivo). Verifica que sea una imagen válida antes de aceptarlo."""
    if not MANUAL.exists():
        return None
    prefix = code.lower() + "."
    candidatos = sorted(
        (p for p in MANUAL.iterdir() if p.is_file() and p.name.lower().startswith(prefix)),
        key=lambda p: len(p.name)  # preferir el nombre más corto (menos extensiones pegadas)
    )
    for p in candidatos:
        try:
            with Image.open(p) as im:
                im.verify()
            return p
        except Exception:
            continue
    return None


def avisar_archivos_sueltos(codes):
    """Avisa sobre archivos en assets/manual/ que no coinciden con ningún ID conocido
    (típicamente por un nombre mal escrito: "C4.jpg" en vez de "C04.jpg")."""
    if not MANUAL.exists():
        return
    prefixes = tuple(f"{c.lower()}." for c in codes)
    sueltos = [p.name for p in MANUAL.iterdir()
               if p.is_file() and p.name != ".gitkeep" and not p.name.lower().startswith(prefixes)]
    if sueltos:
        print("AVISO: en assets/manual/ hay archivos que no coinciden con ningún ID de obra:")
        for n in sueltos:
            print(f"   - {n}  (¿nombre mal escrito? tiene que empezar con el ID exacto, ej: C04...)")
        print()


# ---------------------------------------------------------------------------
# Hoja de control visual
# ---------------------------------------------------------------------------
def write_review(works: list, manifest: dict):
    rows = []
    stamp = int(time.time())
    for w in works:
        m = manifest.get(w["ID"], {})
        st = m.get("status", "MISSING")
        color = {"OK": "#1a7f37", "MANUAL": "#1a7f37", "LOW_RES": "#b58100"}.get(st, "#c62828")
        img = (f'<img src="assets/artworks/{w["ID"]}.jpg?v={stamp}" loading="lazy">'
               if st in ("OK", "MANUAL", "LOW_RES") else '<div class="none">sin imagen</div>')
        rows.append(
            f'<figure>{img}<figcaption><b>{w["ID"]}</b> · {html.escape(w["Título"])}<br>'
            f'<span>{html.escape(w["Artista"])} · {html.escape(str(w.get("Año", "")))}</span><br>'
            f'<i style="color:{color}">{st}</i> <small>{m.get("width", "")}×{m.get("height", "")} · '
            f'{html.escape(m.get("source", ""))}</small></figcaption></figure>')
    REVIEW.write_text(
        "<!doctype html><meta charset=utf-8><title>Revisar imágenes</title><style>"
        "body{font-family:Arial;margin:24px;background:#f3f3ef}h1{font:500 28px Georgia}"
        ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}"
        "figure{margin:0;background:#fff;padding:10px}img{width:100%;height:200px;object-fit:contain;background:#eee}"
        ".none{height:200px;display:flex;align-items:center;justify-content:center;background:#fdd;color:#900}"
        "figcaption{font-size:12px;line-height:1.4;margin-top:6px}span{color:#666}small{color:#888}</style>"
        "<h1>Revisión visual de imágenes</h1><p>Chequeá que cada imagen sea la obra correcta y completa "
        "(no un detalle, no una foto de sala). Si alguna está mal, guardá la correcta como "
        "<code>assets/manual/ID.jpg</code> y volvé a correr DESCARGAR_IMAGENES.bat.</p>"
        f"<div class=g>{''.join(rows)}</div>", encoding="utf-8")


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def run(http: Http, only=None, force: bool = False) -> int:
    works = json.loads(ARTWORKS.read_text(encoding="utf-8"))
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    MANUAL.mkdir(parents=True, exist_ok=True)
    avisar_archivos_sueltos([w["ID"] for w in works])

    if "completar" in CONTACTO:
        print("AVISO: poné tu mail en CONTACTO (tools/fetch_images.py) o en la variable PRUEBA_CONTACTO.")
        print("       Wikimedia es más tolerante con scripts que se identifican.\n")

    todo = []
    for w in works:
        code = w["ID"]
        if only and code not in only:
            continue
        target = OUT / f"{code}.jpg"
        man = manual_file(code)
        if man:
            size = save_web_jpg(man, target)
            manifest[code] = {"status": "MANUAL", "source": f"manual: {man.name}",
                              "width": size[0], "height": size[1]}
            print(f"  {code}: imagen manual aplicada ({size[0]}x{size[1]})")
            continue
        pinned = sources.get(code, {}).get("commons_file")
        stale_pin = bool(pinned) and manifest.get(code, {}).get("file") != pinned
        if (not force and not stale_pin and valid_local(target)
                and manifest.get(code, {}).get("status") in ("OK", "LOW_RES")):
            continue
        todo.append(w)

    print(f"Obras a resolver: {len(todo)} de {len(works)}\n")
    if todo:
        # 1) Artículos de Wikipedia (una llamada agrupada)
        print("Paso 1/4 · buscando artículos de Wikipedia...")
        titles = [t for w in todo for t in sources.get(w["ID"], {}).get("wiki", [])]
        pimg = page_images(http, titles) if titles else {}
        chosen = {}
        for w in todo:
            src = sources.get(w["ID"], {})
            if src.get("commons_file"):
                chosen[w["ID"]] = (src["commons_file"], "Commons (archivo fijado)")
                continue
            for t in src.get("wiki", []):
                if pimg.get(t):
                    chosen[w["ID"]] = (pimg[t], f"Wikipedia: {t}")
                    break

        # 2) Búsqueda en Wikipedia para las que faltan
        pending = [w for w in todo if w["ID"] not in chosen]
        if pending:
            print(f"Paso 2/4 · búsqueda alternativa para {len(pending)} obras...")
            found = {}
            for w in pending:
                q = sources.get(w["ID"], {}).get("search") or f'{w["Título"]} {w["Artista"]}'
                try:
                    found[w["ID"]] = wiki_search(http, q, w)
                except Exception as e:
                    print(f"      {w['ID']}: búsqueda falló ({e})")
            flat = [t for ts in found.values() for t in ts]
            extra = page_images(http, flat) if flat else {}
            for w in pending:
                for t in found.get(w["ID"], []):
                    if extra.get(t):
                        chosen[w["ID"]] = (extra[t], f"Wikipedia (búsqueda): {t}")
                        break
            # 2b) Commons como último recurso (sólo dominio público)
            for w in [w for w in pending if w["ID"] not in chosen]:
                q = sources.get(w["ID"], {}).get("search") or f'{w["Título"]} {w["Artista"]}'
                try:
                    f = commons_search(http, q, w)
                    if f:
                        chosen[w["ID"]] = (f, "Commons (búsqueda)")
                except Exception as e:
                    print(f"      {w['ID']}: búsqueda en Commons falló ({e})")

        # Duplicados: dos obras no pueden compartir archivo
        todo_ids = {w["ID"] for w in todo}
        used = {m.get("file"): c for c, m in manifest.items()
                if c not in todo_ids and m.get("file") and m.get("status") in ("OK", "LOW_RES")}
        for code in sorted(chosen):
            f = chosen[code][0]
            if f in used:
                print(f"      {code}: resolvió al mismo archivo que {used[f]} -> necesita imagen manual")
                del chosen[code]
            else:
                used[f] = code

        print(f"Paso 3/4 · obteniendo URLs de {len(chosen)} imágenes...")
        infos = image_info(http, [f for f, _ in chosen.values()]) if chosen else {}
        print("Paso 4/4 · descargando (con pausas para no saturar a Wikimedia)...\n")
        for i, w in enumerate(todo, 1):
            code = w["ID"]
            tag = f"[{i:02}/{len(todo)}] {code}"
            if code not in chosen or chosen[code][0] not in infos:
                manifest[code] = {"status": "MISSING", "source": chosen.get(code, ("", "no encontrada"))[1]}
                print(f"{tag}: SIN RESOLVER — {w['Título']} ({w['Artista']})")
                continue
            f, how = chosen[code]
            info = infos[f]
            try:
                data = http.get(info["url"], accept="image/jpeg,image/png,image/*;q=0.8", timeout=60)
                size = save_web_jpg(data, OUT / f"{code}.jpg")
                status = "LOW_RES" if max(size) < LOW_RES_PX else "OK"
                manifest[code] = {"status": status, "source": how, "file": f, "repo": info["repo"],
                                  "page": info.get("page"), "width": size[0], "height": size[1]}
                print(f"{tag}: {status} {size[0]}x{size[1]} — {how}")
            except Exception as e:
                manifest[code] = {"status": "ERROR", "source": how, "file": f, "error": str(e)}
                print(f"{tag}: ERROR — {e}")
            MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            http.sleep(PAUSE_DOWNLOAD)

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_review(works, manifest)

    counts, missing = {}, []
    for w in works:
        st = manifest.get(w["ID"], {}).get("status", "MISSING")
        if st in ("OK", "MANUAL", "LOW_RES") and not valid_local(OUT / f"{w['ID']}.jpg"):
            st = "MISSING"
        if st in ("MISSING", "ERROR"):
            missing.append(w["ID"])
        counts[st] = counts.get(st, 0) + 1
    good = counts.get("OK", 0) + counts.get("MANUAL", 0)
    print("\n" + "=" * 64)
    print(f"Listas: {good}  ·  Baja resolución: {counts.get('LOW_RES', 0)}  ·  "
          f"Faltan: {len(missing)}  ·  Total: {len(works)}")
    print(f"Llamadas a Wikimedia en esta corrida: {http.calls}")
    print("Abrí REVISAR_IMAGENES.html y controlá que cada imagen sea la obra correcta.")
    if missing:
        print("Sin imagen:", ", ".join(missing))
        print("Para esas: guardá la imagen a mano en assets/manual/ID.jpg y volvé a ejecutar.")
    return 0 if not missing else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rehacer todas las imágenes")
    ap.add_argument("--only", default="", help="IDs separados por coma, ej: C04,G02")
    args = ap.parse_args()
    only = {x.strip().upper() for x in args.only.split(",") if x.strip()} or None
    return run(Http(), only=only, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
