import geopandas as gpd
import plotly.graph_objects as go
import json


def load_shapefile_as_geojson():
    return


if __name__ == "__main__":
    # geodf = gpd.read_file('/Users/tripham/Documents/Sample_Data/1_shp_files_v2/Housel_v2.shp')

    geodf = gpd.read_file('/Users/tripham/Desktop/satellite-dynamic-report/src/utils/output.shp')

    print(geodf)

    # geodf = geodf.to_crs("WGS84")

    data = geodf.to_json()


    data = json.loads(data)

    print("data", data)

    print(data["features"][0])

    gdf = gpd.GeoDataFrame.from_features(data)
    point = (148.90635, -20.25866)

    import plotly.express as px

    fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": 16,
            "layers": [
                {
                    "source": json.loads(gdf.geometry.to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    fig.show()
