import dash
from dash import html, dcc, Input, Output
import urllib.parse as parse
import ast
from utils import corpus, words_preprocess
from collections import defaultdict
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__)

layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        # content will be rendered in this element
        html.Div(id="page-content"),
    ]
)


def chapter_wise(words, books):
    new_refs = defaultdict(lambda: defaultdict(int))
    for word in words:
        refs = corpus.get(word, [])
        for ref in refs:
            if ref[0] in books:
                new_refs[ref[0]][ref[1]] += 1
    return new_refs


@dash.callback(
    Output("page-content", "children"),
    [Input("url", "search")],
)
def display_page(search):
    data = parse.parse_qs(search.replace("?", ""))
    books = [data.get("book", [""])[0]]
    words = data.get("words", [""])[0]
    words = ast.literal_eval(words)
    if books and words:
        # Make the graph
        words = words_preprocess(words)
        chap_refs = chapter_wise(words, books)  # {"Genesis":{"1":30,"2":20...},"Exodus":{...}...}

        fig = make_subplots(
            rows=len(chap_refs),
            cols=1,
            shared_xaxes=True,
            subplot_titles=[f"{book} - {sum(chap_refs[book].values())} times" for book in books],
        )
        for row, book in enumerate(books):
            x, y = zip(*chap_refs[book].items())
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    customdata=list(zip(x, y)),
                    hovertemplate="Chapter: %{customdata[0]}<br>Word Count: %{customdata[1]}",
                ),
                row=row + 1,
                col=1,
            )

        fig.update_layout(
            height=len(chap_refs) * 400,
            title_text="Chapterwise Combined Counts for words - " + (", ".join(words)),
            yaxis_title="Word Count",
            xaxis_title="Chapters",
            showlegend=False,
        )

        fig.update_xaxes(categoryorder="array", categoryarray=tuple(range(200)))  # Hack for now

        return html.Div([dcc.Graph(figure=fig)])
    else:
        return html.Div("No book or words selected")
