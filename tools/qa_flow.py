#!/usr/bin/env python3
"""Static flow QA for the 24-duel / 7-question schedule."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
qs=json.loads((ROOT/'data/questions.json').read_text(encoding='utf8'))
duels=json.loads((ROOT/'data/duels.json').read_text(encoding='utf8'))
assert len(duels)==24
seen=[]
for i in range(1,25):
    due=[q['id'] for q in qs if q['afterDuel']==i]
    if due: seen += due
assert seen == ['Q01','Q02','Q03','Q04','Q05','Q06','Q07'], seen
assert len(set(q['id'] for q in qs))==7
assert all(q['weight']>0 for q in qs)
print('OK: all 7 questions are reachable at duels 4, 8, 12, 16, 20, 22, 24')
