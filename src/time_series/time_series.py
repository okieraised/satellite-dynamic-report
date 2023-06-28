import io

import pandas as pd

from constants.constants import MINIO_BUCKET
from utils.logging import logger
from utils.minio import Minio_Object

VariableMapper = dict(
    TA="Air Temperature (°C)",
    PAR_mol_day="Photosynthetically Active Radiation (mol/m2/d)",
    SW="Short Wave Radiation",
    P_mm="Precipitation (mm)",
    EVI="Enhanced Vegetation Index",
    LSWI1650="LSWI1650",
    LSWI2105="LSWI2105",
    NDVI="Normalized Difference Vegetation Index",
    blue="Blue",
    green="Green",
    nir="Near-infrared (NIR)",
    red="Red",
    swir1="SWIR 1",
    swir2="SWIR 2",
    temperature_2m="Air Temperature (°C)",
    PAR_mol="Photosynthetically Active Radiation (mol/m2/d)",
)


def query_time_series_data() -> dict:

    res = dict()

    objects = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix='csv')

    logger.info(f"Retrieved {len(objects)} csv objects")

    for obj in objects:
        dropdown_mappers = []

        try:
            key = obj.get('Key')
            site_name = str(key).split("/")[1].capitalize()
            logger.info(f"object site_name: {site_name}")
            raw = Minio_Object.minio_get(key)
            df = pd.read_csv(io.BytesIO(raw), index_col='Date')
            columns = df.columns.tolist()

            for col in columns:
                if VariableMapper.get(col):
                    dropdown_mappers.append({"label": VariableMapper.get(col), "value": col})
            res[site_name] = dict(
                var=dropdown_mappers,
                data=df
            )

        except Exception as err:
            logger.error(f"error retrieving object: {err}")
            continue

    return res


if __name__ == "__main__":
    query_time_series_data()