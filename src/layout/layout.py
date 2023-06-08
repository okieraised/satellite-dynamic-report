import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from dash import dcc, html
from constants.constants import YEARS, DropdownMapper, MapType, Site, MAPBOX_API_KEY, OH_LONG, OH_LAT
from geospatial.shapefile import default_geojson_data
from layout.default_layout import default_data
from time_series.time_series import read_csv
from utils.datetime_utils import get_current_week_number


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
            dcc.Dropdown(options=options, value=value, id=dropdown_id)
        ],
        className='three columns',
        style=dict(width='25%')
    )

    return dropdown


map_layout = dcc.Graph(
    id='heatmap-container',
    style={'marginLeft': '0px',
           'marginRight': '0px',
           'margin-top': '10px',
           'margin-bottom': '0px'},
    figure=dict(
        data=[default_data()],
        layout=go.Layout(
            autosize=True,
            mapbox=dict(
                accesstoken=MAPBOX_API_KEY,
                zoom=6,
                center=dict(lat=OH_LAT, lon=OH_LONG),
                style=MapType.DEFAULT,
                layers=default_geojson_data(),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
        )
    ),
    config=dict(responsive=True, displayModeBar=False)
)


slider_layout = html.Div(
    id="slider-container",
    children=[
        html.Div(
            [
                generate_map_dropdown_menu(dropdown_id="data-dropdown-1",
                                           options=DropdownMapper.SatelliteData,
                                           value="EVI"),
                generate_map_dropdown_menu(dropdown_id="basemap-dropdown",
                                           options=DropdownMapper.WorldMap,
                                           value=MapType.DEFAULT),
                generate_map_dropdown_menu(dropdown_id="week-dropdown",
                                           options=DropdownMapper.WeekNumber,
                                           value=get_current_week_number()),
                generate_map_dropdown_menu(dropdown_id="site-dropdown",
                                           options=DropdownMapper.SiteName,
                                           value=Site.Pratt),
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

graph_layout = dcc.Graph(
    id="selected-data-1",
    figure=dict(
        data=[go.Scatter(x=read_csv()[0], y=read_csv()[1])],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
            title='Housel',
            xaxis={
                'title': dict(
                    text="Year"
                )
            },
            yaxis={
                'title': dict(
                    text="TA"
                )
            }
        ),
    ),
)

graph_layout2 = dcc.Graph(
    id="selected-data-2",
    figure=dict(
        data=[go.Scatter(x=read_csv()[0], y=read_csv()[2])],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
        ),
    ),
)



graph_layout_3 = html.Div(
    [
        dcc.Dropdown(
            options={},
            value="dsdsdsd",
            id="data-dropdown-2",
        ),
        dcc.Graph(
            id="selected-data-3",
            figure=dict(
                data=[go.Scatter(x=[], y=[])],
                layout=dict(
                    paper_bgcolor="#1f2630",
                    plot_bgcolor="#1f2630",
                    font=dict(color="#2cfec1"),
                    autofill=True,
                    margin=dict(t=75, r=50, b=50, l=50),
                    title='Housel',
                    xaxis={
                        'title': dict(
                            text="Year"
                        )
                    },
                    yaxis={
                        'title': dict(
                            text="TA"
                        )
                    }
                ),
            ),
        )
    ],
    className='four columns',
    style=dict(width='48%')
)

graph_layout_4 = html.Div(
    [
        dcc.Dropdown(
            options={},
            value="dsdsdsd",
            id="data-dropdown-3",
        ),
        dcc.Graph(
            id="selected-data-4",
            figure=dict(
                data=[go.Scatter(x=[], y=[])],
                layout=dict(
                    paper_bgcolor="#1f2630",
                    plot_bgcolor="#1f2630",
                    font=dict(color="#2cfec1"),
                    autofill=True,
                    margin=dict(t=75, r=50, b=50, l=50),
                    title='Housel',
                    xaxis={
                        'title': dict(
                            text="Year"
                        )
                    },
                    yaxis={
                        'title': dict(
                            text="TA"
                        )
                    }
                ),
            ),
        )
    ],
    className='four columns',
    style=dict(width='48%')
)