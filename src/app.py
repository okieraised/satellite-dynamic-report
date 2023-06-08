import dash
from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import os
import pandas as pd

from constants.constants import MAPBOX_API_KEY, OK_LONG, OK_LAT, YEARS, MapType, OH_LAT, OH_LONG
from geospatial.shapefile import default_geojson_data
from layout.default_layout import default_data
from layout.layout import map_layout, slider_layout, generate_title_layout, graph_layout, graph_layout2, graph_layout_3, \
    graph_layout_4
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
        generate_title_layout(),
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
        ),
        html.Div(
            id="graph-container-bottom",
            children=[graph_layout_3, graph_layout_4],
        ),
    ]
)


@app.callback(
    Output(component_id='heatmap-container', component_property='figure'),
    Input(component_id='basemap-dropdown', component_property='value')
)
def update_basemap(input_value):
    map_figure = dict(
        data=[default_data()],
        layout=go.Layout(
            autosize=True,
            mapbox=dict(
                accesstoken=MAPBOX_API_KEY,
                zoom=6,
                center=dict(lat=OH_LAT, lon=OH_LONG),
                style=input_value,
                layers=default_geojson_data(),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
        )
    )

    return map_figure


if __name__ == "__main__":
    # import rasterio as rio
    #
    # with rio.open('./sample_data/EVI/2022-07-30.tif') as src:
    #     elevation = src.read(1)
    #     print(elevation)

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


