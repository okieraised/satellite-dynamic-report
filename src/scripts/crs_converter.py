from os import listdir
from os.path import isfile, join

import rasterio as rio
from rasterio.warp import reproject, Resampling, calculate_default_transform

from constants.constants import DEFAULT_CRS


def convert_to_epsg4326(in_dir: str, out_dir: str):
    f_paths = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]

    for f in f_paths:
        try:
            with rio.open(join(in_dir, f)) as src:
                print("process", join(in_dir, f))
                elevation = src.read(1)

                src_transform = src.transform

                # calculate the transform matrix for the output
                dst_transform, width, height = calculate_default_transform(
                    src.crs,
                    DEFAULT_CRS,
                    src.width,
                    src.height,
                    *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
                )

                # set properties for output
                dst_kwargs = src.meta.copy()
                dst_kwargs.update(
                    {
                        "crs": DEFAULT_CRS,
                        "transform": dst_transform,
                        "width": width,
                        "height": height,
                        "nodata": 0,
                    }
                )

                with rio.open(join(out_dir, f), "w", **dst_kwargs) as dst:
                    for i in range(1, src.count + 1):
                        reproject(
                            source=rio.band(src, i),
                            destination=rio.band(dst, i),
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=dst_transform,
                            dst_crs=DEFAULT_CRS,
                            resampling=Resampling.nearest,
                        )
        except Exception as err:
            print(err)
            continue


if __name__ == "__main__":
    in_path = '/Users/tripham/Documents/sample_sat/Housel_VIs'
    out_path = '/Users/tripham/Documents/sample_sat/Housel_VIs2'

    convert_to_epsg4326(in_dir=in_path, out_dir=out_path)