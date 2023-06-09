import dash_leaflet as dl
from dash import Dash, html

app = Dash()
# app.layout = html.Div([
#     dl.Map([dl.TileLayer(), dl.WMSTileLayer(url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
#                                             layers="nexrad-n0r-900913", format="image/png", transparent=True)],
#            center=[40, -100], zoom=4,
#            style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
# ])
GEOTIFF_ID = "geotiff-id"
app.layout = html.Div([
    dl.Map(
        [
            dl.TileLayer(),
            # dl.WMSTileLayer(url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
            #                 layers="nexrad-n0r-900913", format="image/png", transparent=True),
            dl.GeoTIFFOverlay(id=GEOTIFF_ID, band=1, url='/Users/tripham/Desktop/satellite-dynamic-report/src/data/tiff/2022-07-30.tif', interactive=True)
        ],
        zoom=4,
        style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])

if __name__ == '__main__':
    app.run_server()