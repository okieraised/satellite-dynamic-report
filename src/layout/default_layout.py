import plotly.graph_objects as go

from constants.constants import MAPBOX_API_KEY, OK_LAT, OK_LONG, mapbox_style


def default_map_layout() -> go.Layout:
    map_layout = go.Layout(
        autosize=True,
        mapbox=dict(
            accesstoken=MAPBOX_API_KEY,
            zoom=4.5,
            center=dict(lat=OK_LAT, lon=OK_LONG),
            style=mapbox_style,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return map_layout


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
        hoverinfo='text'
    )

    return data


def default_figure() -> dict:
    return dict(
        data=[default_data()],
        layout=default_map_layout()
    )