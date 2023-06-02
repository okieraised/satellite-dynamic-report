import dash
from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import os
import pandas as pd

from constants.constants import MAPBOX_API_KEY, OK_LONG, OK_LAT
from layout.default_layout import default_figure

# Init Dash app
app = dash.Dash(
        __name__,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1"
            }
        ],
        title="Dynamic Report"
    )

server = app.server


app.layout = html.Div(
        dcc.Graph(
            id='map',
            style={'marginLeft': '0px',
                   'marginRight': '0px',
                   'margin-top': '10px',
                   'margin-bottom': '0px'},
            figure=default_figure(),
            config=dict(responsive=True, displayModeBar=False)
        ),
    )


slider_layout = html.Div(
    id="slider-container",
    children=[
        html.P(
            id="slider-text",
            children="Drag the slider to change the year:",
        ),
        dcc.Slider(
            id="years-slider",
            min=min(YEARS),
            max=max(YEARS),
            value=min(YEARS),
            marks={
                str(year): {
                    "label": str(year),
                    "style": {"color": "#7fafdf"},
                }
                for year in YEARS
            },
        ),
    ],
)

app.layout = slider_layout

if __name__ == "__main__":
    app.run_server(debug=True, port=18050, processes=1, threaded=True)


