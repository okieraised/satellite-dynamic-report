import dash
from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import os
import pandas as pd

from constants.constants import MAPBOX_API_KEY, OK_LONG, OK_LAT, YEARS, MapType
from layout.default_layout import default_figure
from layout.layout import map_layout, slider_layout, title_layout, graph_layout, graph_layout2
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
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[slider_layout, map_layout],
                ),
                html.Div(
                    id="graph-container",
                    children=[graph_layout, graph_layout2],
                ),
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=18050, processes=1, threaded=True)


'''
Absolutely, the data will be available in a server, it can be AWS or Microsoft.  
The data types are TIFF, .shp, and .csv.   
There will be a folder with the data for each week 1to52 and other folder with historic data. 
 The TIFF data represents different layers of information and ideally, we would like that the dynamic report displays 
 one of the layers in a map, but having the option to choose different layers.  In addition, to display the different 
 layer values when moving the cursor over the map and when clicking in a region generating the graphs for that layer.  
 The graphs would be YeartoDate value and comparison with the historic value for that pixel. 
 The other graph will be the field average and how it compares to that pixel value in the year to date.
'''


