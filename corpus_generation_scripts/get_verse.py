import json

from bs4 import BeautifulSoup

file = "NIV.xml"

ref = "1 Kings 10:28"
ref = "2 Chronicles 1:16"

k = ref.rsplit(" ", 1)
i = k[1].split(":")
ref = [k[0], i[0], i[1]]
print(ref)
with open(file, "r") as f:
    soup = BeautifulSoup(f, "xml")

# TODO Use monad & currying to prevent None linter hits
book = soup.find("b", {"n": ref[0]})
chap = book.find("c", {"n": ref[1]})
verse = chap.find("v", {"n": ref[2]})
print(verse.text)
