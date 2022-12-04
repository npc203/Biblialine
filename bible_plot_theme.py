from bs4 import BeautifulSoup
import re
from collections import namedtuple,defaultdict,Counter
from string import punctuation

file = "NIV.xml"
word = "(?i)lord"

Ref = namedtuple("Ref", "book chapter verse word")

with open(file, "r") as f:
    soup = BeautifulSoup(f, "xml")

text = (''.join(s.findAll(text=True))for s in soup.findAll('v'))

c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))
print (c.most_common(30))

input("a")

def getRef(word):
    verse = word.parent
    chapter = verse.parent
    book = chapter.parent
    return Ref(book["n"], chapter["n"], verse["n"], word)

res = soup.findAll(text=re.compile(word))
print("size:",len(res))
stats = defaultdict(int)
for ele in res:
    stats[getRef(ele).book]+=1

myList = stats.items()
x, y = zip(*myList)

import plotly.express as px
fig = px.bar(x=x,y=y)
fig.show()
