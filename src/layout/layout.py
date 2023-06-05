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
        # html.P(
        #     id="slider-text",
        #     children="Drag the slider to change the year:",
        # ),
        dcc.Dropdown(
            options=[
                {
                    "label": "Histogram of total number of deaths (single year)",
                    "value": "show_absolute_deaths_single_year",
                },
                {
                    "label": "Histogram of total number of deaths (1999-2016)",
                    "value": "absolute_deaths_all_time",
                },
                {
                    "label": "Age-adjusted death rate (single year)",
                    "value": "show_death_rate_single_year",
                },
                {
                    "label": "Trends in age-adjusted death rate (1999-2016)",
                    "value": "death_rate_all_time",
                },
            ],
            value="show_death_rate_single_year",
            id="map-dropdown",
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
        data=[dict(x=0, y=0)],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
        ),
    ),
)

graph_layout2 = dcc.Graph(
    id="selected-data-2",
    figure=dict(
        data=[dict(x=0, y=0)],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
        ),
    ),
)