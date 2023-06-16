from constants.constants import MINIO_BUCKET
from utils.datetime_utils import get_week_number
from utils.logging import logger
from utils.minio import Minio_Object


def get_obj_path(data_type: str, site_name: str) -> list:
    prefix = f'{data_type}/{site_name}/'.lower()
    default_data_paths = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix=prefix)
    objs = [i['Key'] for i in default_data_paths]
    logger.info(f"got {len(objs)} objects")
    return objs


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