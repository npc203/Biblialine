import json
import difflib
from rapidfuzz import process, fuzz

with open("corpus.json") as f:
    d = json.load(f)

l = tuple(d.keys())
for word in l:
    x = [p for p in process.extract(word, l, scorer=fuzz.QRatio, limit=50)[1:] if p[1] > 85]
    if x:
        print("-" * 20, "\n", word, len(x))
        for p in x:
            print(p, end=" ")
        print()
