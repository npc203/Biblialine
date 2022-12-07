from bs4 import BeautifulSoup
import re
from collections import defaultdict, namedtuple
import json

file = "NIV.xml"

Ref = namedtuple("Ref", "book chapter verse word")

# with open(file, "r") as f:
#     soup = BeautifulSoup(f, "xml")


# def getRef(word):
#     verse = word.parent
#     chapter = verse.parent
#     book = chapter.parent
#     return Ref(book["n"], chapter["n"], verse["n"], word)


# corpus = defaultdict(list)
# for verse in soup.findAll("v"):
#     ref = getRef(next(verse.children))
#     for word in verse.text.lower().split():
#         corpus[word].append((ref.book, ref.chapter, ref.verse))

from tabulate import tabulate
import plotly.express as px

with open("corpusv2.json", "r") as f:
    corpus = json.load(f)

one_words = []
for w, refs in corpus.items():
    if len(refs) == 1:
        curr_ref = refs[0]
        one_words.append((w, f"{curr_ref[0]} {curr_ref[1]}:{curr_ref[2]}"))

freq = defaultdict(int)
for word, ref in one_words:
    freq[ref[0]] += 1

x, y = zip(*freq.items())
fig = px.bar(
    x=x, y=y, title="Books with unique words", labels={"y": "Number of unique words", "x": "books"}
)
# fig.show()

open("actual_uniquev2.txt", "w").write(tabulate(one_words))
