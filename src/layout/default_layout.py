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


def default_shapefile():
    geodf = gpd.read_file('/Users/tripham/Documents/Sample_Data/1_shp_files_v2/Housel_v2.geojson')

    data = geodf.to_json()
    data = json.loads(data)
    gdf = gpd.GeoDataFrame.from_features(data)
    point = (148.90635, -20.25866)

    return {
        "source": json.loads(gdf.geometry.to_json()),
        "below": "traces",
        "type": "line",
        "color": "purple",
        "line": {"width": 1.5},
    }
