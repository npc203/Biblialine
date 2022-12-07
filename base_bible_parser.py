# http://www.opensong.org/home/download
# Scroll down to the bibles section and get those zip files, which are just xmls

from bs4 import BeautifulSoup
import re
from collections import defaultdict, namedtuple
import json
import contractions

file = "NIV.xml"

Ref = namedtuple("Ref", "book chapter verse word")

with open(file, "r") as f:
    soup = BeautifulSoup(f, "xml")

word = "bless"


def getRef(word):
    verse = word.parent
    chapter = verse.parent
    book = chapter.parent
    return Ref(book["n"], chapter["n"], verse["n"], word)


# res = soup.findAll(text=re.compile(word))
# for ele in res:
#     print(getRef(ele).book)

# print(len(res))
# print(soup.text)

from nltk import word_tokenize
from nltk.corpus import stopwords
import string

stop = set(stopwords.words("english"))
# x = [i for i in word_tokenize(soup.text.lower()) if i not in stop]

corpus = defaultdict(list)
for verse in soup.findAll("v"):
    ref = getRef(next(verse.children))
    # Verse processing
    sentence = verse.text.lower()
    sentence = contractions.fix(sentence)
    # Hypens are bad sometimes
    sentence = sentence.replace("-", " ")
    sentence = re.sub(r"[^a-zA-Z0-9\s]", "", sentence)
    sentence = word_tokenize(sentence)
    sentence = [i for i in sentence if i not in stop]
    # print(sentence)

    for word in sentence:
        if word not in stop:
            corpus[word].append((ref.book, ref.chapter, ref.verse))

json.dump(corpus, open("corpusv2.json", "w"))
