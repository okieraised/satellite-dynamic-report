import plotly.graph_objects as go
import geopandas as gpd
import json

from constants.constants import MAPBOX_API_KEY, OK_LAT, OK_LONG, MapType, OH_LONG, OH_LAT
from geospatial.shapefile import default_geojson_data


def default_map_layout() -> go.Layout:
    map_layout = go.Layout(
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

    # import plotly.express as px
    #
    # fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
    #     mapbox={
    #         "accesstoken": MAPBOX_API_KEY,
    #         "style": MapType.DEFAULT,
    #         "zoom": 16,
    #         "layers": [
    #             {
    #                 "source": json.loads(gdf.geometry.to_json()),
    #                 "below": "traces",
    #                 "type": "line",
    #                 "color": "purple",
    #                 "line": {"width": 1.5},
    #             }
    #         ],
    #     },
    #     margin={"l": 0, "r": 0, "t": 0, "b": 0},
    # )
    #
    # fig.show()