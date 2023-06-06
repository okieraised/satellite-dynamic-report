import plotly.graph_objects as go
import geopandas as gpd

from constants.constants import MAPBOX_API_KEY, OK_LAT, OK_LONG, MapType


def default_map_layout() -> go.Layout:
    map_layout = go.Layout(
        autosize=True,
        mapbox=dict(
            accesstoken=MAPBOX_API_KEY,
            zoom=4.5,
            center=dict(lat=OK_LAT, lon=OK_LONG),
            style=MapType.DEFAULT,
            layers=[
                dict(
                    sourcetype='raster',
                    source='sample_data/EVI/2022-07-30.tif',
                )
            ],


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
        hoverinfo='text',
    )

    return data


# fig= px.imshow(elevation, color_continuous_scale=bamako)
# my_layout= dict(title_text='Big Tujunga Cachement-California', title_x=0.5, width =700, height=500, template='none',
#                   coloraxis_colorbar=dict(len=0.75, thickness=25))
# fig.update_layout(**my_layout)


def default_figure() -> dict:
    return dict(
        data=[default_data()],
        layout=default_map_layout()
    )