import numpy as np
import plotly.graph_objs as go
import rasterio as rio
import plotly.express as px
from matplotlib.colors import LightSource

with rio.open('../data/tiff/2022-07-30.tif') as src:
    elevation = src.read(1)


if __name__ == "__main__":
    with rio.open('../data/tiff/2022-07-30.tif') as src:
        elevation = src.read(1)
        print(elevation)

        fig = px.imshow(elevation)
        my_layout = dict(title_text='Big Tujunga Cachement-California', title_x=0.5, width=700, height=500,
                         template='none',
                         coloraxis_colorbar=dict(len=0.75, thickness=25))
        fig.update_layout(**my_layout)

        fig.show()