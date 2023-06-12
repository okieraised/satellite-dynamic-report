import numpy as np
import plotly.graph_objs as go
import rasterio as rio
import plotly.express as px
from matplotlib.colors import LightSource

from rasterio.coords import BoundingBox
from rasterio import windows
from rasterio import warp
from rasterio import mask

import geopandas as gpd

def reverse_coordinates(pol):
    """
    Reverse the coordinates in pol
    Receives list of coordinates: [[x1,y1],[x2,y2],...,[xN,yN]]
    Returns [[y1,x1],[y2,x2],...,[yN,xN]]
    """
    return [list(f[-1::-1]) for f in pol]

def to_index(wind_):
    """
    Generates a list of index (row,col): [[row1,col1],[row2,col2],[row3,col3],[row4,col4],[row1,col1]]
    """
    return [[wind_.row_off,wind_.col_off],
            [wind_.row_off,wind_.col_off+wind_.width],
            [wind_.row_off+wind_.height,wind_.col_off+wind_.width],
            [wind_.row_off+wind_.height,wind_.col_off],
            [wind_.row_off,wind_.col_off]]

def generate_polygon(bbox):
    """
    Generates a list of coordinates: [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x1,y1]]
    """
    return [[bbox[0],bbox[1]],
             [bbox[2],bbox[1]],
             [bbox[2],bbox[3]],
             [bbox[0],bbox[3]],
             [bbox[0],bbox[1]]]

def pol_to_np(pol):
    """
    Receives list of coordinates: [[x1,y1],[x2,y2],...,[xN,yN]]
    """
    return np.array([list(l) for l in pol])

def pol_to_bounding_box(pol):
    """
    Receives list of coordinates: [[x1,y1],[x2,y2],...,[xN,yN]]
    """
    arr = pol_to_np(pol)
    return BoundingBox(np.min(arr[:,0]),
                       np.min(arr[:,1]),
                       np.max(arr[:,0]),
                       np.max(arr[:,1]))

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