import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from dash import dcc, html
from constants.constants import YEARS, DropdownMapper, MapType
from layout.default_layout import default_figure
from time_series.time_series import read_csv
from utils.datetime_utils import get_current_week_number

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

map_layout = dcc.Graph(
    id='heatmap-container',
    style={'marginLeft': '0px',
           'marginRight': '0px',
           'margin-top': '10px',
           'margin-bottom': '0px'},
    figure=default_figure(),
    config=dict(responsive=True, displayModeBar=False)
)


slider_layout = html.Div(
    id="slider-container",
    children=[
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            options=DropdownMapper.SatelliteData,
                            value="EVI",
                            id="data-dropdown",
                        ),
                    ],
                    className='three columns',
                    style=dict(width='25%')

                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=DropdownMapper.WorldMap,
                            value=MapType.DEFAULT,
                            id="basemap-dropdown",
                        ),
                    ],
                    className='three columns',
                    style=dict(width='25%')
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=DropdownMapper.WeekNumber,
                            value=get_current_week_number(),
                            id="week-dropdown",
                        ),
                    ],
                    className='three columns',
                    style=dict(width='25%')
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=DropdownMapper.SiteName,
                            value="",
                            id="site-dropdown",
                        ),
                    ],
                    className='three columns',
                    style=dict(width='25%')
                )
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

graph_layout_3 = dcc.Graph(
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

graph_layout_4 = dcc.Graph(
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