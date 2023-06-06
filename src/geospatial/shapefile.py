import geopandas as gpd
import plotly.graph_objects as go
import json


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

    # import plotly.express as px
    #
    # fig = px.choropleth(data["features"], geojson=data["features"], locations='type', color='type',
    #                     color_continuous_scale="Viridis",
    #                     range_color=(0, 12),
    #                     scope="usa",
    #                     labels={'unemp': 'unemployment rate'}
    #                     )
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.show()

    # fig = px.choropleth_mapbox(geodf,
    #      geojson=geodf.geometry,
    #      locations=geodf.index,
    #      color="Name",
    #      # center={"lat": point[1], "lon": point[0]},
    #      mapbox_style="open-street-map",
    #      zoom=16)
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.show()



    # fig = go.Figure(go.Choroplethmapbox(geojson=json.loads(geodf.to_json()),
    #                                     locations=geodf.index, z=geodf['Name'],
    #                                     colorscale="Viridis"))
    #
    # fig.update_layout(mapbox_style="open-street-map",
    #                   height=1000,
    #                   autosize=True,
    #                   margin={"r": 0, "t": 0, "l": 0, "b": 0},
    #                   paper_bgcolor='#303030',
    #                   plot_bgcolor='#303030',
    #                   mapbox=dict(zoom=9), # center=dict(lat=60.1699, lon=24.9384),
    #                   )
    #
    # fig.show()
