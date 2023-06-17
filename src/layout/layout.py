import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

from dash import dcc, html
import dash_leaflet as dl
from constants.constants import YEARS, DropdownMapper, MapType, Site, MAPBOX_API_KEY, OH_LONG, OH_LAT, DEFAULT_SITE, \
    OK_LAT, OK_LONG, BASEMAP_URL, DEFAULT_DATA
from layout.default_layout import default_data
from time_series.time_series import VariableMapper
from utils.datetime_utils import get_current_week_number
from utils.query_data import get_aggregate_of_data


def generate_title_layout() -> html.Div:
    title_layout = html.Div(
        id="title",
        children=[
            dbc.Row(
                [html.H1("Satellite Dynamic Report Viewer")],
                justify="center",
                align="center",
                className="h-50",
            )
        ],
        style={
            'width': '100%',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center'
        }
    )

    return title_layout


def generate_map_dropdown_menu(dropdown_id: str, options: any, value: any) -> html.Div:
    dropdown = html.Div(
        [
            dcc.Dropdown(options=options, value=value, id=dropdown_id, clearable=False, multi=False)
        ],
        className='three columns',
        style=dict(width='25%')
    )

    return dropdown


def render_basemap(map_type: str, geojson_urls: list = None) -> dl.Map:
    map_layer_children = [dl.TileLayer(url=BASEMAP_URL.format(map_style=map_type, access_token=MAPBOX_API_KEY))]

    if geojson_urls:
        for geojson_url in geojson_urls:
            map_layer_children.append(dl.GeoJSON(url=geojson_url))

    map_layout = dl.Map(
        id='heatmap-container',
        style={'marginLeft': '0px',
               'marginRight': '0px',
               'margin-top': '10px',
               'margin-bottom': '0px'},
        children=map_layer_children,
        zoom=6,
        center=(OH_LAT, OH_LONG),
    )

    return map_layout


slider_layout = html.Div(
    id="slider-container",
    children=[
        html.Div(
            [
                generate_map_dropdown_menu(dropdown_id="data-type-dropdown",
                                           options=DropdownMapper.SatelliteData,
                                           value=DEFAULT_DATA),
                generate_map_dropdown_menu(dropdown_id="basemap-dropdown",
                                           options=DropdownMapper.WorldMap,
                                           value=MapType.DEFAULT),
                generate_map_dropdown_menu(dropdown_id="week-dropdown",
                                           options=DropdownMapper.WeekNumber,
                                           value=get_current_week_number()),
                generate_map_dropdown_menu(dropdown_id="site-dropdown",
                                           options=DropdownMapper.SiteName,
                                           value=DEFAULT_SITE),
            ],
            className='row',
            style={
                'display': 'flex',
                'width': '100%',
            }

        ),

        dcc.Slider(
            id="slider",
            min=min(YEARS),
            max=max(YEARS),
            value=max(YEARS),
            step=1,
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


def generate_default_graph_layout() -> dict:
    default_layout = dict(
        data=[go.Scatter(x=[], y=[])],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
            title='N/A',
            xaxis={
                'title': dict(
                    text="N/A"
                )
            },
            yaxis={
                'title': dict(
                    text="N/A"
                )
            }
        ),
    )

    return default_layout


def generate_default_histogram_graph() -> dcc.Graph:
    graph_layout = dcc.Graph(
        id="selected-data-1",
        figure=generate_default_graph_layout(),
    )

    return graph_layout


def generate_aggregate_figure(data: list, xaxis: str = "N/A", yaxis: str = "N/A", title: str = "N/A"):

    figure = dict(
        data=data,
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            margin=dict(t=75, r=50, b=50, l=50),
            title={
                'text': title,
                'x': 0.5
            },
            xaxis={
                'title': dict(
                    text=xaxis
                ),
                'tickformat': '%Y-%m-%d'
            },
            yaxis={
                'title': dict(
                    text=yaxis
                )
            }
        )
    )

    return figure


def generate_aggregate_graph(data: pd.DataFrame, xaxis: str = "N/A", yaxis: str = "N/A", title: str = "N/A"):
    if data.empty:
        fig_data = [go.Scatter(x=[], y=[])]
    else:
        fig_data = [go.Scatter(x=data.index.tolist(), y=data[col_name].tolist(), name=col_name, mode="markers")
                    for col_name in data.columns]

    graph_layout = dcc.Graph(
        id="selected-data-2",
        figure=generate_aggregate_figure(data=fig_data, xaxis=xaxis, yaxis=yaxis, title=title)
    )

    return graph_layout


def generate_time_series_graph_by_site(dropdown_id: str, graph_id: str, data: dict, site_name: Site = DEFAULT_SITE):
    # Init variables
    dropdown_options = {}
    dropdown_value = list(VariableMapper.keys())[0]
    x_axis_title = "Year"
    y_axis_title = VariableMapper.get(dropdown_value)

    # Retrieve actual data
    site_data = data.get(site_name, None)
    if not site_data:
        raise Exception(f"Site {site_name} not found.")

    dropdown_options = site_data["var"]

    default_option = dropdown_options[0]

    dropdown_value = default_option["value"]
    y_axis_title = default_option["label"]

    df = site_data["data"]

    graph_layout = html.Div(
        [
            dcc.Dropdown(
                options=dropdown_options,
                value=dropdown_value,
                id=dropdown_id,
                clearable=False,
                multi=False
            ),
            dcc.Graph(
                id=graph_id,
                figure=dict(
                    data=[go.Scatter(x=df.index.tolist(), y=df[dropdown_value].tolist())],
                    layout=dict(
                        paper_bgcolor="#1f2630",
                        plot_bgcolor="#1f2630",
                        font=dict(color="#2cfec1"),
                        autofill=True,
                        margin=dict(t=75, r=50, b=50, l=50),
                        title=f"Time Series of {y_axis_title} of {site_name}",
                        xaxis={
                            'title': dict(
                                text=x_axis_title
                            )
                        },
                        yaxis={
                            'title': dict(
                                text=y_axis_title
                            )
                        }
                    ),
                ),
            )
        ],
        className='four columns',
        style=dict(width='48%')
    )

    return graph_layout
