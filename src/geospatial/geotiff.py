import numpy as np
import plotly.graph_objs as go
import rasterio as rio
import plotly.express as px
from matplotlib.colors import LightSource

from rasterio.coords import BoundingBox
from rasterio import windows
from rasterio import warp
from rasterio import mask
from rasterio.warp import reproject, Resampling, calculate_default_transform


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


class GeoTiffObject(object):

    def __init__(self, url: str):
        self.url = url

    def read(self):
        return





    def x(self):
        return


with rio.open('../data/tiff/2022-07-30.tif') as src:
    elevation = src.read(1)

    array = src.read()
    print(array.shape)


if __name__ == "__main__":

    dst_crs = "EPSG:4326"

    # with rio.open('../data/tiff/2022-07-30-2.tif') as src:
    #     elevation = src.read(1)
    #     print(elevation)
    #
    #     array = src.read()
    #     print(array.shape)
    #     print("src", array.max())
    #
    #     px_vals = []

        # for x in range(elevation.shape[0]):
        #     for y in range(elevation.shape[1]):
        #         px_vals.append({'x': x,
        #                         'y': y,
        #                         'value': elevation[x, y]})
        #
        # print(px_vals)
        #
        # print(px_vals[0])
        #
        # print()

    from os import listdir
    from os.path import isfile, join

    mypath = '/Users/tripham/Documents/sample_sat/Housel_VIs'
    outpath = '/Users/tripham/Documents/sample_sat/Housel_VIs2'

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print(onlyfiles)

    for f in onlyfiles:
        with rio.open(join(mypath, f)) as src:
            print("process", join(mypath, f))
            elevation = src.read(1)

            src_transform = src.transform

            # calculate the transform matrix for the output
            dst_transform, width, height = calculate_default_transform(
                src.crs,
                dst_crs,
                src.width,
                src.height,
                *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
            )

            # set properties for output
            dst_kwargs = src.meta.copy()
            dst_kwargs.update(
                {
                    "crs": dst_crs,
                    "transform": dst_transform,
                    "width": width,
                    "height": height,
                    "nodata": 0,  # replace 0 with np.nan
                }
            )

            with rio.open(join(outpath, f), "w", **dst_kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rio.band(src, i),
                        destination=rio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=dst_transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.nearest,
                    )


    # with rio.open('../data/tiff/tz850.tiff') as src:
    #     elevation = src.read(1)
    #     print(elevation)
    #
    #     input_crs = src.crs
    #     input_gt = src.transform
    #
    #     print(f"input_crs: {input_crs}")
    #     print(f"input_gt: {input_gt}")
    #
    #     src_transform = src.transform
    #
    #     # calculate the transform matrix for the output
    #     dst_transform, width, height = calculate_default_transform(
    #         src.crs,
    #         dst_crs,
    #         src.width,
    #         src.height,
    #         *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
    #     )
    #
    #     # set properties for output
    #     dst_kwargs = src.meta.copy()
    #     dst_kwargs.update(
    #         {
    #             "crs": dst_crs,
    #             "transform": dst_transform,
    #             "width": width,
    #             "height": height,
    #             "nodata": 0,  # replace 0 with np.nan
    #         }
    #     )
    #
    #     with rio.open("../data/tiff/tz850-2.tiff", "w", **dst_kwargs) as dst:
    #         for i in range(1, src.count + 1):
    #             reproject(
    #                 source=rio.band(src, i),
    #                 destination=rio.band(dst, i),
    #                 src_transform=src.transform,
    #                 src_crs=src.crs,
    #                 dst_transform=dst_transform,
    #                 dst_crs=dst_crs,
    #                 resampling=Resampling.nearest,
    #             )
