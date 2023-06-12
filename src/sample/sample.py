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
color_domain = dict(domainMin=0.1, domainMax=2.0, colorscale=['white', 'orange', 'red'])
# dl.Colorbar(width=200, height=20, min=0.00001, max=0.15, position="topleft", tickDecimals=2, unit=" ",
#                        colorscale=['white', 'orange', 'red'], style={"color":"white"})],
#                        id='raster2',center=(-16.394, -62.024), zoom=13, style={'width': '100%', 'height': '92.8vh'})
# color_domain = dict(domainMin=1392, domainMax=1550, colorscale=['white', 'orange', 'red'])

app.layout = html.Div([

    dl.Map(
        style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"},
       zoom=5,
       children=[
           dl.TileLayer(),
           dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True,
                             url="/Users/tripham/Desktop/satellite-dynamic-report/src/data/tiff/2022-07-30-2.tif",
                             band=2, opacity=0.8,
                             **color_domain),
           dl.Colorbar(width=200, height=20, min=0.1, max=2.0, position="topleft", tickDecimals=2, unit=" ",
                       colorscale=['white', 'orange', 'red'], style={"color": "white"}),
       ]),
    # dl.Map(
    #     [
    #         dl.TileLayer(),
    #         # dl.WMSTileLayer(url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
    #         #                 layers="nexrad-n0r-900913", format="image/png", transparent=True),
    #         dl.GeoTIFFOverlay(id=GEOTIFF_ID, opacity=0.8, band=1,
    #                           url='/Users/tripham/Desktop/satellite-dynamic-report/src/data/tiff/tz850.tiff', # 2022-07-30-2
    #                           interactive=True, **color_domain)
    #     ],
    #     zoom=4,
    #     style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])

if __name__ == '__main__':
    app.run_server()