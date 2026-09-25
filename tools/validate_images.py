#!/usr/bin/env python3
"""Validate local artwork image files and report missing/invalid files."""
from __future__ import annotations
import json
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    Image = None
ROOT=Path(__file__).resolve().parents[1]
works=json.loads((ROOT/'data/artworks.json').read_text(encoding='utf-8'))
missing=[]; invalid=[]; ok=[]
for w in works:
    p=ROOT/w.get('image_file','')
    if not p.exists(): missing.append((w['ID'],str(p.relative_to(ROOT)))) ; continue
    if p.stat().st_size<10000: invalid.append((w['ID'],'too small')); continue
    if Image:
        try:
            with Image.open(p) as im:
                im.verify()
            with Image.open(p) as im:
                if max(im.size)<700: print(f"  AVISO {w['ID']}: baja resolucion {im.size[0]}x{im.size[1]} (sirve, pero conviene reemplazarla)")
        except Exception as e:
            invalid.append((w['ID'],str(e))); continue
    ok.append(w['ID'])
print(f'OK: {len(ok)}')
print(f'Missing: {len(missing)}')
for x in missing: print('  MISSING',*x)
print(f'Invalid: {len(invalid)}')
for x in invalid: print('  INVALID',*x)
raise SystemExit(0 if not missing and not invalid else 2)
