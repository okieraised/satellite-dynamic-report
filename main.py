import dash
from dash import html, dcc

import plotly.express as px
import geopandas as gpd

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server


def main_map():

    map = html.Div(
            #className="eight columns",
            children=[
                # Time series graph
                dcc.Graph(
                    id='integrated-basin4',
                    #className="eight columns",
                    figure={
                        'layout': {'plot_bgcolor': '#21252C',
                        'paper_bgcolor': '#21252C',
                        },
                    },
                    config={"scrollZoom": True,
                            "displayModeBar": True
                    },
                    style={'height':'710px',
                    },
                ),
            ],
            style={'marginLeft': '0px',
                   'marginRight': '0px',
                   'margin-top': '10px',
                   'margin-bottom': '0px'}
            )

    return map

def main():
    geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    px.set_mapbox_access_token(open(".env").read())
    fig = px.scatter_mapbox(geo_df,
                            lat=geo_df.geometry.y,
                            lon=geo_df.geometry.x,
                            hover_name="name",
                            zoom=1)
    fig.show()

layout = html.Div(
    id="Main Container",
    children=[
        main_map()
    ]
)

app.layout = layout

if __name__ == "__main__":
    main()
    # app.run_server(debug=True)