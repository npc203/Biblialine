from dash import Dash, dcc, html, Input, Output, State
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly
from collections import defaultdict
from utils import (
    words_preprocess,
    bible_books_in_order,
    unique_word_count,
    HOVER_TEMPLATE,
    corpus,
    all_words,
    plot_word,
    plot_words,
    chapter_wise,
)
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import plotly.express as px

app = dash.get_app()
dash.register_page(__name__, path="/")


def callback_processor(data):
    words = words_preprocess(data["words"])
    fig, dfs = plot_words(
        words=words,
        corpus=corpus,
        filter_books=data["books"],
        show_percent=data.get("show_percent"),
    )
    return fig, dfs


layout = html.Div(
    [
        html.H1("Biblialine"),
        html.Div(
            [
                dcc.Dropdown(all_words, multi=True, id="word-dropdown"),
                dcc.Checklist(["Show Percentage"], ["Show Percentage"], id="options"),
            ]
        ),
        html.Br(),
        html.Div(id="my-output"),
        dcc.Loading(
            [
                dcc.Graph(id="combined-graph", figure=go.Figure()),
                dcc.Graph(id="main-graph", figure=go.Figure()),
            ]
        ),
        html.Div(id="sus", style={"white-space": "pre-line"}),
        dbc.Modal(
            [
                dbc.ModalHeader("Chapter-wise word count"),
                dbc.ModalBody(dcc.Graph(id="modal-graph", figure=go.Figure())),
                # dbc.ModalFooter(dbc.Button("CLOSE BUTTON", id="close", className="ml-auto")),
            ],
            id="modal",
            size="xl",
        ),
    ]
)


@app.callback(
    [
        Output("combined-graph", "clickData"),
        Output("main-graph", "clickData"),
        Output("modal", "is_open"),
        Output("modal-graph", "figure"),
    ],
    [Input("combined-graph", "clickData"), Input("main-graph", "clickData")],
    State("word-dropdown", "value"),
    State("modal", "is_open"),
)
def show_chapter_graph(combined_G, main_G, words, modal):
    if combined_G or main_G:
        data = combined_G or main_G
        book = data["points"][0]["label"]
        books = [book]
        # Make the graph
        print(words)
        words = words_preprocess(words)
        df = chapter_wise(words, books)  # {"Genesis":{"1":30,"2":20...},"Exodus":{...}...}

        fig = px.bar(
            df, x="chapter", y="count", color="word", hover_data=["word", "count", "verses"]
        )

        fig.update_layout(
            yaxis_title="Word Count",
            xaxis_title="Chapters",
            showlegend=True,
        )

        fig.update_xaxes(categoryorder="array", categoryarray=tuple(range(200)))  # Hack for now

        return None, None, True, fig
        # return dcc.Location(id="url", href=f"/chapters?book={book}&words={words}")
    return None, None, False, go.Figure()


@app.callback(
    [
        Output(component_id="combined-graph", component_property="figure"),
        Output(component_id="main-graph", component_property="figure"),
    ],
    Input("word-dropdown", "value"),
    Input("options", "value"),
)
def update_graph(words, options):
    if words:
        words = [words] if isinstance(words, str) else words
        show_percent = "Show Percentage" in options
        words_fig, dfs = callback_processor(
            {
                "books": bible_books_in_order,
                "words": words,
                "show_percent": show_percent,
            }
        )

        fig = px.bar(
            dfs,
            x="book",
            y="percent" if show_percent else "count",
            color="word",
            hover_data=["book", "count", "percent"],
        )

        fig.update_layout(
            title="Combined frequency for words - " + (", ".join(words)),
            yaxis_title="Percentage (%)" if show_percent else "Word Count",
            xaxis_title="Books",
        )
        fig.update_xaxes(categoryorder="array", categoryarray=bible_books_in_order)

        # Update colors for the separate graphs
        colors = {g.name: g.marker.color for g in fig.data}
        for g in words_fig.data:
            g.marker.color = colors[g.name]

        return fig, (words_fig if len(words) > 1 else go.Figure())
    return go.Figure(), go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True)
