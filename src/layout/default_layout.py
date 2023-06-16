import plotly.graph_objects as go
import geopandas as gpd
import json

from constants.constants import MAPBOX_API_KEY, OK_LAT, OK_LONG, MapType, OH_LONG, OH_LAT


def default_data() -> go.Scattermapbox:
    data = go.Scattermapbox(
        lat=[OK_LAT],
        lon=[OK_LONG],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=0,
            color='blue',
            opacity=0.7
        ),
        hoverinfo='text',
    )

    return data


def generate_default_time_series_fig() -> dict:
    default_time_series_fig = dict(
        data=[go.Scatter(x=[], y=[])],
        layout=dict(
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            autofill=True,
            margin=dict(t=75, r=50, b=50, l=50),
            title="",
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

    return default_time_series_fig
