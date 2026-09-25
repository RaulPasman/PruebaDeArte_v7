import json,sys
from pathlib import Path
root=Path(__file__).parent
A=json.loads((root/'data/artworks.json').read_text())
D=json.loads((root/'data/duels.json').read_text())
P=json.loads((root/'data/profiles.json').read_text())
Q=json.loads((root/'data/questions.json').read_text())
S=json.loads((root/'data/scoring.json').read_text())
assert len(A)==60 and len({x['ID'] for x in A})==60
assert len(D)==24 and len({x['id'] for x in D})==24
assert all(x['a'] in {a['ID'] for a in A} and x['b'] in {a['ID'] for a in A} for x in D)
assert len(P)==10 and len(Q)==7
for x in A:
    for ax in ['E1 Abstracto↔Figurativo','E2 Estructurado↔Espontáneo','E3 Sereno↔Expresivo','E4 Contenido↔Saturado','E5 Plano↔Material','E6 Cotidiano↔Imaginario','E7 Íntimo↔Dominante','E8 Transparente↔Conceptual']:
        assert -1<=x[ax]<=1
for p in P:
    assert all(-1<=p['vector'][ax]<=1 for ax in p['vector'])
print('OK: 60 obras / 24 duelos / 10 perfiles / 7 preguntas / 8 ejes')
