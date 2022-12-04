from collections import defaultdict
import json
from collections import defaultdict, Counter

with open("corpus.json", "r") as f:
    corpus = json.load(f)

stats = defaultdict(list)
for word, refs in corpus.items():
    stats[word].append(len(refs))

print(Counter(stats).most_common(50))
