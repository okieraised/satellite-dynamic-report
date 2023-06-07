import geopandas as gpd
import plotly.graph_objects as go
import json

from constants.constants import MapType, MAPBOX_API_KEY
from utils.file import list_file_with_same_ext


def default_geojson_data() -> [dict]:
    res = []

    f_geojson = list_file_with_same_ext('/Users/tripham/Desktop/satellite-dynamic-report/src/data/geojson', '.geojson')

    for f_path in f_geojson:
        geodf = gpd.read_file(f_path)
        data = geodf.to_json()
        data = json.loads(data)
        gdf = gpd.GeoDataFrame.from_features(data)

        elem = {
            "source": json.loads(gdf.geometry.to_json()),
            "below": "traces",
            "type": "line",
            "color": "green",
            "line": {"width": 3},
        }

        res.append(elem)

    return res


if __name__ == "__main__":
    default_geojson_data()
    # geodf = gpd.read_file('/Users/tripham/Documents/Sample_Data/1_shp_files_v2/Housel_v2.geojson')
    #
    # # geodf = gpd.read_file('/Users/tripham/Desktop/satellite-dynamic-report/src/utils/output.shp')
    #
    # print(geodf)
    #
    # # geodf = geodf.to_crs("WGS84")
    #
    # data = geodf.to_json()
    #
    #
    # data = json.loads(data)
    #
    # print("data", data)
    #
    # print(data["features"][0])
    #
    # gdf = gpd.GeoDataFrame.from_features(data)
    # point = (148.90635, -20.25866)
    #
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
