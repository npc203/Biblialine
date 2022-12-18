import json
from collections import Counter, defaultdict
from re import L

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request
from plotly.subplots import make_subplots

from utils import bible_books_in_order, words_preprocess

app = Flask(__name__)
with open("corpusv2.json", "r") as f:
    corpus = json.load(f)

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


# GRAPHING STUFF
from collections import defaultdict

HOVER_TEMPLATE = "Book: %{customdata[0]}<br>Word Count: %{customdata[1]}<br>Percentage: %{y}%"


def plot_word(main_word, corpus, filter_books=None, show_percent=False):
    stats = defaultdict(int)
    for ref in corpus[main_word]:
        if filter_books:
            if ref[0] in filter_books:
                stats[ref[0]] += 1
        else:
            stats[ref[0]] += 1

    # expanded = [(book, count), (book, count), ...]
    expanded = list(stats.items())
    custom_data = expanded.copy()
    if show_percent:
        expanded = [(i, j / unique_word_count[i] * 100) for i, j in stats.items()]

    x, y = zip(*expanded)
    bar = go.Bar(x=x, y=y, customdata=custom_data, hovertemplate=HOVER_TEMPLATE)
    return bar


def plot_words(words, corpus, filter_books=None, show_percent=False):
    fig = make_subplots(
        rows=len(words),
        cols=1,
        shared_xaxes=True,
        subplot_titles=tuple(map(lambda x: "Word: " + x, words)),
    )
    for row, main_word in enumerate(words):
        fig.add_trace(plot_word(main_word, corpus, filter_books, show_percent), row=row + 1, col=1)

    fig.update_layout(
        height=len(words) * 350,
        title_text="Word Frequency",
        showlegend=False,
        yaxis_title="Percentage" if show_percent else "Word Count",
        xaxis_title="Books",
    )
    fig.update_xaxes(categoryorder="array", categoryarray=bible_books_in_order)
    return fig


def chapter_wise(words, books):
    new_refs = defaultdict(lambda: defaultdict(int))
    for word in words:
        refs = corpus.get(word, [])
        for ref in refs:
            if ref[0] in books:
                new_refs[ref[0]][ref[1]] += 1
    return new_refs


# Callbacks
def callback_processor(data) -> str:
    words = words_preprocess(data["words"])
    fig = plot_words(
        words=words,
        corpus=corpus,
        filter_books=data["books"],
        show_percent=data.get("show_percent"),
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# Remove redundancy?
def chapter_callback(word, book):
    words = words_preprocess([word]) if isinstance(word, str) else words_preprocess(word)
    refs = chapter_wise(words, [book])
    x, y = zip(*refs[book].items())
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            customdata=list(zip(x, y)),
            hovertemplate="Chapter: %{customdata[0]}<br>Word Count: %{customdata[1]}",
        ),
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# Server routing
@app.route("/")
def main_page():
    return render_template(
        "index.html",
        graphJSON=callback_processor({"books": [], "words": ["magic", "wax"]}),
        valid_words=list(corpus.keys()),
    )


# Callback routes
@app.route("/callback", methods=["GET", "POST"])
def update_graph():
    # TODO carefully parse the data!
    data = request.args.get("data")
    graphJSON = callback_processor(data)
    return graphJSON


@app.route("/chapter_callback", methods=["GET", "POST"])
def chapter_callback_route():
    data = request.args.to_dict()
    return chapter_callback(data["words"], data["book"])


app.run(debug=True)
