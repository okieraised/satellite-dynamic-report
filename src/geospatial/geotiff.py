import io
import os.path
import numpy as np
import rasterio as rio

from rasterio.coords import BoundingBox
from rasterio import windows
from rasterio import warp
from rasterio import mask
from rasterio.warp import reproject, Resampling, calculate_default_transform

import geopandas as gpd

import utils.logging
from constants.constants import MINIO_ENDPOINT_URL, MINIO_BUCKET
from utils.datetime_utils import get_week_number
from utils.logging import logger
from utils.minio import Minio_Object


class GeoTiffObject(object):

    def __init__(self, obj: str):
        self.obj = obj
        self.logger = logger
        self.data = self.get_minio_data()[0]
        self.pixels = []
        self.crs = "EPSG:4326"
        self.center = self.get_minio_data()[1]

    def gen_url(self) -> str:
        url = "/".join([MINIO_ENDPOINT_URL, MINIO_BUCKET, self.obj])
        return url

    def get_minio_data(self):
        try:
            img_raw = Minio_Object.minio_get(self.obj)
            img_bytes = io.BytesIO(img_raw)
            with rio.open(img_bytes) as src:
                center = src.xy(src.height // 2, src.width // 2)
                return src.read(1), (center[1], center[0])

        except Exception as err:
            logger.error(f"{err}")
            return [], (0, 0)


    def get_pixels(self):
        px_vals = []

        if len(self.data) == 0:
            return px_vals

        for x in range(self.data.shape[0]):
            for y in range(self.data.shape[1]):
                px_vals.append(self.data[x, y])

        return px_vals

    def min_pix(self) -> float:
        try:
            min_pix = self.data.min()
            return min_pix
        except Exception as err:
            logger.error(f"{err}")
            return 0

    def max_pix(self) -> float:
        try:
            max_pix = self.data.max()
            return max_pix
        except Exception as err:
            logger.error(f"{err}")
            return 0

    def generate_color_scheme(self) -> dict:

        min_val = self.min_pix()
        max_val = self.max_pix()

        color_domain = dict(domainMin=min_val, domainMax=max_val, colorscale=['green', 'yellow', 'red'])
        return color_domain

    def get_current_week(self) -> int:
        try:
            f_name = os.path.basename(self.obj)
            f_name_wo_ext = os.path.splitext(f_name)[0]
            year, month, day = f_name_wo_ext.split("-")
            week_number = get_week_number(int(year), int(month), int(day))

            return week_number
        except Exception as err:
            logger.error(f"{err}")
            return 0

    def get_bounding_box(self):
        return BoundingBox(np.min(self.data[:, 0]),
                           np.min(self.data[:, 1]),
                           np.max(self.data[:, 0]),
                           np.max(self.data[:, 1]))


if __name__ == "__main__":
    tif = GeoTiffObject('vi/housel/2000-01-01.tif')
    print(tif.gen_url())
    print(tif.get_pixels())
    print(tif.get_current_week())
    print(tif.get_bounding_box())
    print(tif.get_minio_data())







    # dst_crs = "EPSG:4326"
    #
    # raw = Minio_Object.minio_get('/vi/housel/2000-01-01.tif')
    # raw_img = io.BytesIO(raw)
    #
    # with rio.open(raw_img) as src:
    #     elevation = src.read(1)
    #     print("here", elevation)
    #
    #     print("min", elevation.min())
    #
    # p = 'http://localhost:9000/dynamic-data/evi/housel/2022-07-30.tif'
    # print(p.split('dynamic-data'))





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

    # from os import listdir
    # from os.path import isfile, join
    #
    # mypath = '/Users/tripham/Documents/sample_sat/Housel_VIs'
    # outpath = '/Users/tripham/Documents/sample_sat/Housel_VIs2'
    #
    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #
    # print(onlyfiles)
    #
    # for f in onlyfiles:
    #     with rio.open(join(mypath, f)) as src:
    #         print("process", join(mypath, f))
    #         elevation = src.read(1)
    #
    #         src_transform = src.transform
    #
    #         # calculate the transform matrix for the output
    #         dst_transform, width, height = calculate_default_transform(
    #             src.crs,
    #             dst_crs,
    #             src.width,
    #             src.height,
    #             *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
    #         )
    #
    #         # set properties for output
    #         dst_kwargs = src.meta.copy()
    #         dst_kwargs.update(
    #             {
    #                 "crs": dst_crs,
    #                 "transform": dst_transform,
    #                 "width": width,
    #                 "height": height,
    #                 "nodata": 0,  # replace 0 with np.nan
    #             }
    #         )
    #
    #         with rio.open(join(outpath, f), "w", **dst_kwargs) as dst:
    #             for i in range(1, src.count + 1):
    #                 reproject(
    #                     source=rio.band(src, i),
    #                     destination=rio.band(dst, i),
    #                     src_transform=src.transform,
    #                     src_crs=src.crs,
    #                     dst_transform=dst_transform,
    #                     dst_crs=dst_crs,
    #                     resampling=Resampling.nearest,
    #                 )

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
