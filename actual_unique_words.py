from bs4 import BeautifulSoup
import re
from collections import defaultdict, namedtuple
import json

file = "NIV.xml"

Ref = namedtuple("Ref", "book chapter verse word")

with open(file, "r") as f:
    soup = BeautifulSoup(f, "xml")


def getRef(word):
    verse = word.parent
    chapter = verse.parent
    book = chapter.parent
    return Ref(book["n"], chapter["n"], verse["n"], word)


corpus = defaultdict(list)
for verse in soup.findAll("v"):
    ref = getRef(next(verse.children))
    for word in verse.text.lower().split():
        corpus[word].append((ref.book, ref.chapter, ref.verse))

from tabulate import tabulate
import plotly.express as px

one_words = []
for w, refs in corpus.items():
    if len(refs) == 1:
        one_words.append((w, refs[0]))

freq = defaultdict(int)
for word, ref in one_words:
    freq[ref[0]] += 1

x, y = zip(*freq.items())
fig = px.bar(
    x=x, y=y, title="Books with unique words", labels={"y": "Number of unique words", "x": "books"}
)
fig.show()

open("actual_unique.txt", "w").write(tabulate(one_words))