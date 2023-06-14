import io

import dash_leaflet as dl
from dash import Dash, html, dcc

from constants.constants import MAPBOX_API_KEY
from utils.minio import Minio_Object

app = Dash()

GEOTIFF_ID = "geotiff-id"
color_domain = dict(domainMin=-210.30674846625766, domainMax=443.45394736842104, colorscale=['blue', 'orange', 'red'])
# color_domain = dict(domainMin=20, domainMax=40, colorscale=['blue', 'orange', 'red'])
# color_domain = dict(domainMin=0.00001, domainMax=0.15, colorscale=['white', 'orange', 'red'])



mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/dark-v11/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"


# url=mapbox_url.format(id="satellite-streets-v10", access_token=mapbox_access_token) heatmap-container
url = 'http://localhost:9000/dynamic-data/evi/housel/2022-07-30.tif'
url = 'http://127.0.0.1:9000/dynamic-data/evi/housel/2015-02-03.tif'
url2 = 'http://localhost:9000/dynamic-data/shapefile/housel/Housel_v2.geojson'
app.layout = html.Div([
            dcc.Location(id="url", refresh=True),
            dl.Map([
                       dl.GeoTIFFOverlay(id="raster", interactive=True, url=url, band=0, opacity=0.5,**color_domain),
                        dl.GeoJSON(id="json", url=url2)
                       # dl.Colorbar(width=200, height=20, min=0.1, max=1.99, position="topleft", tickDecimals=2, unit=" ",
                       # colorscale=['white', 'orange', 'red'], style={"color":"white"})
                    ], id='raster2', center=(41.865053, -80.789809), zoom=13, style={'width': '100%', 'height': '92.8vh'})
                ])

if __name__ == '__main__':
    app.run_server()

    dl.Map(id="", children=[dl.TileLayer()])