import numpy as np
import plotly.graph_objs as go
import rasterio as rio
import plotly.express as px
from matplotlib.colors import LightSource

import geopandas as gpd

with rio.open('../data/tiff/2022-07-30.tif') as src:
    elevation = src.read(1)


if __name__ == "__main__":
    # with gpd.read_file('../data/tiff/2022-07-30.tif') as src:
    #     elevation = src.read()
    #
    #     print(elevation)

    with rio.open('../data/tiff/2022-07-30.tif') as src:
        elevation = src.read(1)
        print(elevation)

        input_crs = src.crs
        input_gt = src.transform

        print(f"input_crs: {input_crs}")
        print(f"input_gt: {input_gt}")



        # fig = px.imshow(elevation)
        # my_layout = dict(title_text='Big Tujunga Cachement-California', title_x=0.5, width=700, height=500,
        #                  template='none',
        #                  coloraxis_colorbar=dict(len=0.75, thickness=25))
        # fig.update_layout(**my_layout)
        #
        # fig.show()