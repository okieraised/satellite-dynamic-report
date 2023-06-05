import dash
from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import os
import pandas as pd

from constants.constants import MAPBOX_API_KEY, OK_LONG, OK_LAT, YEARS
from layout.layout import map_layout, slider_layout, title_layout
import dash_bootstrap_components as dbc


app = dash.Dash(
        __name__,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1"
            }
        ],
        title="Dynamic Report",
    )

server = app.server


left_side_layout = html.Div(
    id="left-side-map",
    children=[
        slider_layout,
        map_layout
    ]
)



app.layout = html.Div(
    id="root",
    children=[
        title_layout,
        left_side_layout
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=18050, processes=1, threaded=True)


