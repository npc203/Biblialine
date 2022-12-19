OT = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
]

NT = [
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]

bible_books_in_order = OT + NT

import json
from collections import defaultdict


def words_preprocess(words):
    return [w.lower() for w in words]


HOVER_TEMPLATE = (
    "Book: %{customdata[0]}<br>Word Count: %{customdata[1]}<br>Percentage:  %{customdata[2]}"
)

with open("corpusv2.json", "r") as f:
    corpus = json.load(f)

all_words = list(corpus.keys())

# Unique Word count, needed for percent stuff
book_word_variance = defaultdict(
    lambda: defaultdict(int)
)  # {"Genesis":{"beginning":30,..},"Exodus":{...}...}
for word, refs in corpus.items():
    for ref in refs:
        book_word_variance[ref[0]][word] += 1

unique_word_count = {
    i: sum(c for c in j.values()) for i, j in book_word_variance.items()
}  # {"Genesis": total_word_count ,"Exodus": 3000}

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


def plot_word(main_word, corpus, filter_books=None, show_percent=False):
    stats = defaultdict(int)
    for ref in corpus[main_word]:
        if filter_books:
            if ref[0] in filter_books:
                stats[ref[0]] += 1
        else:
            stats[ref[0]] += 1

    df = pd.DataFrame(stats.items(), columns=["book", "count"])
    df["percent"] = df.apply(
        lambda row: row["count"] / unique_word_count[row["book"]] * 100, axis=1
    )
    df["word"] = main_word

    bar = px.bar(
        df,
        x="book",
        y="percent" if show_percent else "count",
        hover_data=["book", "count", "percent"],
    )
    bar.update_traces(name=main_word)
    return bar, df


def plot_words(words, corpus, filter_books=None, show_percent=False):
    fig = make_subplots(
        rows=len(words),
        cols=1,
        shared_xaxes=True,
        subplot_titles=tuple(map(lambda x: "Word: " + x, words)),
    )
    big_df = pd.DataFrame()
    for row, main_word in enumerate(words):
        bar, df = plot_word(main_word, corpus, filter_books, show_percent)
        fig.add_trace(bar.data[0], row=row + 1, col=1)
        big_df = pd.concat([big_df, df], axis=0)

    fig.update_layout(
        height=len(words) * 350,
        title_text="Word Frequency",
        yaxis_title="Percentage (%)" if show_percent else "Word Count",
        xaxis_title="Books",
    )
    fig.update_xaxes(categoryorder="array", categoryarray=bible_books_in_order)
    return fig, big_df


def chapter_wise(words, books):
    cols = ["book", "chapter", "word", "count", "verses"]
    df = pd.DataFrame(columns=cols)
    for word in words:
        new_refs = defaultdict(lambda: [0, set()])  # (count,verses)
        refs = corpus.get(word, [])
        for ref in refs:
            if ref[0] in books:
                pt = new_refs[(ref[0], ref[1])]
                pt[0] += 1
                pt[1].add(int(ref[2]))
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        (book, chap, word, count, ", ".join(map(str, sorted(verses))))  # Cursed
                        for (book, chap), (count, verses) in new_refs.items()
                    ],
                    columns=cols,
                ),
            ],
            ignore_index=True,
        )
        print(df)
    return df
