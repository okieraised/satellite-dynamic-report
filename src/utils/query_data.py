from constants.constants import MINIO_BUCKET, DataType, Site
from geospatial.geotiff import GeoTiffObject
from utils.datetime_utils import get_week_number, validate_file_format
from utils.logging import logger
from utils.minio import Minio_Object

import pandas as pd


def get_obj_path(data_type: str, site_name: str) -> list:
    prefix = f'{data_type}/{site_name}/'.lower()
    default_data_paths = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix=prefix)
    objs = [i['Key'] for i in default_data_paths]
    logger.info(f"got {len(objs)} objects")
    return objs


def get_aggregate_of_data(data_type: str, site_name: str):
    df = pd.DataFrame()

    res = dict(date=[], min=[], max=[], avg=[])

    prefix = f'{data_type}/{site_name}/'.lower()
    o_paths = get_obj_path(data_type=data_type, site_name=site_name)

    if len(o_paths) > 0:
        for o_path in o_paths:
            f_path = o_path.split(prefix)[1]
            try:
                d_date = str(f_path).split('.')[0]
                if not validate_file_format(d_date):
                    continue

                tif_data = GeoTiffObject(o_path)
                max_pix = tif_data.max_pix()
                min_pix = tif_data.min_pix()
                avg_pix = tif_data.avg_pix()

                res.get('date').append(d_date)
                res.get('min').append(float(f"{min_pix:.2f}"))
                res.get('max').append(float(f"{max_pix:.2f}"))
                res.get('avg').append(float(f"{avg_pix:.2f}"))

            except Exception as err:
                logger.error(f"{err}")
                continue

        try:
            df = pd.DataFrame.from_dict(res)
            df = df.set_index('date')
            return df
        except Exception as err:
            logger.error(f"{err}")
            return df

    return df


def map_data_path_to_week(data_type: str, site_name: str, year: int) -> dict:
    prefix = f'{data_type}/{site_name}/'.lower()

    res = dict()
    objs = get_obj_path(data_type=data_type, site_name=site_name)

    if len(objs) > 0:
        file_paths = [i.split(prefix)[1] for i in objs]
        for f_path in file_paths:
            try:
                base = str(f_path).split('.')[0]
                time_component = base.split('-')
                d_year = int(time_component[0])
                d_month = int(time_component[1])
                d_day = int(time_component[2])

                if d_year != year:
                    continue

                week_number = get_week_number(d_year, d_month, d_day)
                res.update({week_number: f_path})

            except Exception as err:
                logger.error(f"{err}")
                continue

    logger.debug(f"data: {res}")

    return res


if __name__ == "__main__":
    objects = get_aggregate_of_data(DataType.EVI, Site.Housel)
    print(objects)
