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
from layout.layout import map_layout, slider_layout, generate_title_layout, graph_layout, graph_layout2, \
    graph_layout_4, generate_time_series_graph_by_site
import dash_bootstrap_components as dbc

from time_series.time_series import query_time_series_data, VariableMapper
from utils.logging import logger

csv_data = query_time_series_data()


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
            children=[
                generate_time_series_graph_by_site(dropdown_id="data-dropdown-2", graph_id="selected-data-3", data=csv_data),
                graph_layout_4],
        ),
    ]
)


########################################################################################################################
# Callback
########################################################################################################################

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


@app.callback(
    Output(component_id='selected-data-3', component_property='figure'),
    [
        Input(component_id='data-dropdown-2', component_property='value'),
        Input(component_id='site-dropdown', component_property='value'),
    ]
)
def update_time_series_graph(variable_input, site_input):

    logger.info(f"variable_input: {variable_input} | site_input: {site_input}")

    # print(f"data_input: {variable_input}")
    # print(f"site_input: {site_input}")

    # Init variables
    dropdown_options = {}
    # dropdown_value = list(VariableMapper.keys())[0]
    # x_axis_title = "Year"
    # y_axis_title = VariableMapper.get(dropdown_value)
    #
    # # Retrieve actual data
    # site_data = data.get(site_name, None)
    # if not site_data:
    #     raise Exception(f"Site {site_name} not found.")
    #
    # dropdown_options = site_data["var"]
    #
    # default_option = dropdown_options[0]
    #
    # dropdown_value = default_option["value"]
    # y_axis_title = default_option["label"]
    #
    # df = site_data["data"]




    fig = dict(
        data=[go.Scatter(x=[], y=[])],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
            title=f"Time series data for {site_input}",
            xaxis={
                'title': dict(
                    text="year"
                )
            },
            yaxis={
                'title': dict(
                    text="asd"
                )
            }
        )
    )

    return fig

    # return
    # map_figure = dict(
    #     data=[default_data()],
    #     layout=go.Layout(
    #         autosize=True,
    #         mapbox=dict(
    #             accesstoken=MAPBOX_API_KEY,
    #             zoom=6,
    #             center=dict(lat=OH_LAT, lon=OH_LONG),
    #             style=input_value,
    #             layers=default_geojson_data(),
    #         ),
    #         margin=dict(l=0, r=0, t=0, b=0),
    #     )
    # )
    #
    # return map_figure

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


