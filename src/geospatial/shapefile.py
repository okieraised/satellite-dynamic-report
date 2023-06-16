import geopandas as gpd
import json
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