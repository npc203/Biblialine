import difflib
import json

from rapidfuzz import fuzz, process


def similar_words(word, list_words, percent):
    x = [
        p
        for p in process.extract(word, list_words, scorer=fuzz.QRatio, limit=50)[1:]
        if p[1] > percent
    ]
    print(x)


with open("corpusv2.json") as f:
    d = json.load(f)

l = tuple(d.keys())
word = input("Enter word:")
similar_words(word, l, 50)
