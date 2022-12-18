from dash import Dash, dcc, html, Input, Output, State
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly

app = Dash(__name__)
from collections import defaultdict
from utils import words_preprocess, bible_books_in_order

HOVER_TEMPLATE = "Book: %{customdata[0]}<br>Word Count: %{customdata[1]}<br>Percentage: %{y}%"

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


def callback_processor(data):
    words = words_preprocess(data["words"])
    fig = plot_words(
        words=words,
        corpus=corpus,
        filter_books=data["books"],
        show_percent=data.get("show_percent"),
    )
    return fig


app.layout = html.Div(
    [
        html.H1("Biblialine"),
        html.Div(
            [
                html.H5("Input Words:"),
                dcc.Dropdown(all_words, multi=True, id="word-dropdown"),
                dcc.Checklist(["Show Percentage"], ["Show Percentage"], id="options"),
                html.Button("Go", id="submit-val", n_clicks=0),
            ]
        ),
        html.Br(),
        html.Div(id="my-output"),
        dcc.Graph(id="combined-graph", figure=go.Figure()),
        dcc.Graph(id="main-graph", figure=go.Figure()),
    ]
)


@app.callback(
    [
        Output(component_id="combined-graph", component_property="figure"),
        Output(component_id="main-graph", component_property="figure"),
    ],
    Input("submit-val", "n_clicks"),
    State("word-dropdown", "value"),
    State("options", "value"),
)
def update_graph(n_clicks, words, options):
    if n_clicks > 0 and words:
        words = [words] if isinstance(words, str) else words
        show_percent = "Show Percentage" in options
        words_fig = callback_processor(
            {
                "books": bible_books_in_order,
                "words": words,
                "show_percent": show_percent,
            }
        )

        # Re-extract data from graph
        big_data = words_fig.to_dict()

        all_percents = defaultdict(float)
        all_counts = defaultdict(int)

        # for each word graph add percentages together
        for word_graph in big_data["data"]:
            count = list(map(lambda x: x[1], word_graph["customdata"]))
            percents = word_graph["y"]
            books = word_graph["x"]
            for i in range(len(books)):
                all_percents[books[i]] += percents[i]
                all_counts[books[i]] += count[i]

        word_books, all_percentages_from_y = zip(*all_percents.items())

        print(len(word_books), len(all_percentages_from_y))
        bar = go.Bar(
            x=word_books,
            y=all_percentages_from_y,
            hovertemplate=HOVER_TEMPLATE,
            customdata=list(all_counts.items()),
        )
        fig = go.Figure(data=bar)
        fig.update_layout(
            title="Combined frequency for words - " + (", ".join(words)),
            showlegend=False,
            yaxis_title="Percentage" if show_percent else "Word Count",
            xaxis_title="Books",
        )
        fig.update_xaxes(categoryorder="array", categoryarray=bible_books_in_order)

        return fig, words_fig
    return go.Figure(), go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True)
