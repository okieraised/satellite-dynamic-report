import dash_bootstrap_components as dbc

from dash import dcc, html
from constants.constants import YEARS
from layout.default_layout import default_figure

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

map_layout = html.Div(
    id="map-container",
    children=[
        html.P(
            id="map-text",
            children="",
        ),
        dcc.Graph(
            id='map',
            style={'marginLeft': '0px',
                   'marginRight': '0px',
                   'margin-top': '10px',
                   'margin-bottom': '0px'},
            figure=default_figure(),
            config=dict(responsive=True, displayModeBar=False)
        ),
    ]
)

slider_layout = html.Div(
    id="slider-container",
    children=[
        html.P(
            id="slider-text",
            children="Drag the slider to change the year:",
        ),
        dcc.Slider(
            id="slider",
            min=min(YEARS),
            max=max(YEARS),
            value=min(YEARS),
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
