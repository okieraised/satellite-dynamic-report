import dash
from dash import Dash, dcc, html, Input, Output
import dash_leaflet as dl

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import os
import pandas as pd

from constants.constants import MAPBOX_API_KEY, OK_LONG, OK_LAT, YEARS, MapType, OH_LAT, OH_LONG, BASEMAP_URL, \
    MINIO_BUCKET, DEFAULT_DATA, DEFAULT_SITE, CURRENT_YEAR
from geospatial.geotiff import GeoTiffObject
from geospatial.shapefile import default_geojson_data
from layout.default_layout import default_data, generate_default_time_series_fig
from layout.layout import slider_layout, generate_title_layout, graph_layout_2, \
    generate_time_series_graph_by_site, render_basemap, generate_default_histogram_graph, \
    generate_default_histogram_layout
import dash_bootstrap_components as dbc

from time_series.time_series import query_time_series_data, VariableMapper
from utils.datetime_utils import get_week_number
from utils.logging import logger
from utils.minio import Minio_Object
from utils.query_data import map_data_path_to_week

csv_data = query_time_series_data()
# prefix = f'{DEFAULT_DATA}/{DEFAULT_SITE}/'.lower()


# def get_obj_path(data_type: str, site_name: str) -> list:
#     prefix = f'{data_type}/{site_name}/'.lower()
#     default_data_paths = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix=prefix)
#     objs = [i['Key'] for i in default_data_paths]
#     logger.info(f"got {len(objs)} objects")
#     return objs
#
#
# def map_data_path_to_week(data_type: str, site_name: str, year: int) -> dict:
#     prefix = f'{data_type}/{site_name}/'.lower()
#
#     res = dict()
#     objs = get_obj_path(data_type=data_type, site_name=site_name)
#
#     if len(objs) > 0:
#         file_paths = [i.split(prefix)[1] for i in objs]
#         for f_path in file_paths:
#             try:
#                 base = str(f_path).split('.')[0]
#                 time_component = base.split('-')
#                 d_year = int(time_component[0])
#                 d_month = int(time_component[1])
#                 d_day = int(time_component[2])
#
#                 if d_year != year:
#                     continue
#
#                 week_number = get_week_number(d_year, d_month, d_day)
#                 res.update({week_number: f_path})
#
#             except Exception as err:
#                 logger.error(f"{err}")
#                 continue
#
#     logger.debug(f"data: {res}")
#
#     return res


app = dash.Dash(
        __name__,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1"
            }
        ],
        title="Dynamic Report",
        suppress_callback_exceptions=True,
        prevent_initial_callbacks=True,
    )

server = app.server

app.layout = html.Div(
    id="root",
    children=[
        generate_title_layout(),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[slider_layout, render_basemap(map_type=MapType.DEFAULT)],
                ),
                html.Div(
                    id="graph-container",
                    children=[generate_default_histogram_graph(), graph_layout_2],
                ),
            ]
        ),
        html.Div(
            id="graph-container-bottom",
            children=[
                generate_time_series_graph_by_site(dropdown_id="data-dropdown-2", graph_id="selected-data-3", data=csv_data),
                generate_time_series_graph_by_site(dropdown_id="data-dropdown-3", graph_id="selected-data-4", data=csv_data)],
        ),
    ]
)




########################################################################################################################
# Callback
########################################################################################################################

@app.callback(
    [
        Output(component_id='heatmap-container', component_property='children'),
        Output(component_id='selected-data-1', component_property='figure')
    ],
    [
        Input(component_id="slider", component_property="value"),
        Input(component_id="data-type-dropdown", component_property="value"),
        Input(component_id="week-dropdown", component_property="value"),
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id='basemap-dropdown', component_property='value')

    ],
    prevent_initial_call=True
)
def update_basemap(year: int, data_type: str, week_number: int, site_name: str, input_map_style):

    logger.info(f"year: {year} | data_type: {data_type} | week_number: {week_number} | site_name: {site_name} | "
                f"input_map_value: {input_map_style}")

    map_figure = [dl.TileLayer(url=BASEMAP_URL.format(map_style=input_map_style, access_token=MAPBOX_API_KEY))]

    default_hist = generate_default_histogram_layout()

    try:
        data_mapper = map_data_path_to_week(data_type=data_type, site_name=site_name, year=year)

        file_name = data_mapper.get(week_number)

        if file_name:
            prefix = f'{data_type}/{site_name}/'.lower()
            obj_path = ''.join([prefix, file_name])
            logger.info(f"rendering object {obj_path}")

            tif_data = GeoTiffObject(obj_path)
            tif_url = tif_data.gen_url()
            tif_color_scale = tif_data.generate_color_scheme()
            logger.info(f"geotiff url: {tif_url}")
            logger.info(f"geotiff max_pix: {tif_data.max_pix()} | geotiff min_pix: {tif_data.min_pix()} | "
                        f"geotiff center: {tif_data.center}")

            map_figure = [
                dl.Map(children=[
                    dl.TileLayer(url=BASEMAP_URL.format(map_style=input_map_style, access_token=MAPBOX_API_KEY)),
                    dl.GeoTIFFOverlay(id="raster", interactive=True, url=tif_url, band=0, opacity=0.5,
                                      **tif_color_scale),
                    dl.Colorbar(width=200, height=20, min=tif_color_scale.get('domainMin'),
                                max=tif_color_scale.get('domainMax'),
                                position="bottomleft",
                                tickDecimals=2, unit=" ",
                                colorscale=tif_color_scale.get('colorscale'),
                                style={"color": tif_color_scale.get('colorscale')[0]})
                ],
                    center=tif_data.center, zoom=20)
            ]

            figure = dict(
                data=[go.Histogram(x=tif_data.get_pixels(), nbinsx=20)],
                layout=dict(
                    paper_bgcolor="#1f2630",
                    plot_bgcolor="#1f2630",
                    font=dict(color="#2cfec1"),
                    autofill=True,
                    margin=dict(t=75, r=50, b=50, l=50),
                    title=f"Distribution of pixel values for {data_type} at {site_name}",
                    xaxis={
                        'title': dict(
                            text="Value"
                        ),
                    },
                    yaxis={
                        'title': dict(
                            text="Count",
                        ),
                        'type': 'log'
                    }
                )
            )

            return map_figure, figure

        return map_figure, default_hist

    except Exception as err:
        logger.error(f"{err}")
        return map_figure, default_hist


@app.callback(
    [
        Output(component_id="app-container", component_property="children")
    ],
    [
        Input(component_id="raster", component_property='click_lat_lng_val')
    ],
    allow_duplicate=True,
)
def show_pixel(click_lat_lng):
    try:
        if not click_lat_lng:
            raise dash.exceptions.PreventUpdate("cancel the callback")

        lat = click_lat_lng[0]
        long = click_lat_lng[1]
        value = click_lat_lng[2]

        print(lat, long, value)
        raise dash.exceptions.PreventUpdate("cancel the callback")
    except Exception as err:
        logger.error(f"{err}")
        raise dash.exceptions.PreventUpdate("No value found. Cancel the callback")



@app.callback(
    [
        Output(component_id='selected-data-3', component_property='figure'),
        Output(component_id='data-dropdown-2', component_property='options'),
    ],
    [
        Input(component_id='data-dropdown-2', component_property='value'),
        Input(component_id='site-dropdown', component_property='value'),
    ],
    prevent_initial_call=True
)
@app.callback(
    [
        Output(component_id='selected-data-4', component_property='figure'),
        Output(component_id='data-dropdown-3', component_property='options'),
    ],
    [
        Input(component_id='data-dropdown-3', component_property='value'),
        Input(component_id='site-dropdown', component_property='value'),
    ],
    prevent_initial_call=True
)
def update_time_series_graph(variable_input, site_input):

    logger.info(f"variable_input: {variable_input} | site_input: {site_input}")

    try:
        site_data = csv_data.get(site_input, None)

        # If no site data is available -> return blank map
        if not site_data:
            logger.error(f"Site {site_input} not found.")
            return generate_default_time_series_fig(), []

        site_options = site_data["var"]
        if not site_options:
            logger.error(f"Site {site_input} has no options.")
            return generate_default_time_series_fig(), []

        site_df = site_data["data"]
        if site_df.empty:
            logger.error(f"Site {site_input} has no data.")
            return generate_default_time_series_fig(), []

        y_axis_title = VariableMapper.get(variable_input)

        fig = dict(
            data=[go.Scatter(x=site_df.index.tolist(), y=site_df[variable_input].tolist())],
            layout=dict(
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                autofill=True,
                margin=dict(t=75, r=50, b=50, l=50),
                title=f"Time Series of {y_axis_title} of {site_input}",
                xaxis={
                    'title': dict(
                        text="Year"
                    )
                },
                yaxis={
                    'title': dict(
                        text=y_axis_title
                    )
                }
            )
        )

        return fig, site_options
    except Exception as err:
        logger.error(f"{err}")
        return generate_default_time_series_fig(), []


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


