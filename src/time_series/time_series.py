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
    swir2="SWIR 2"
)


def read_csv():
    df = pd.read_csv('/Users/tripham/Desktop/satellite-dynamic-report/src/data/csv/Housel_DD_Input.csv', index_col='Date')

    return [df.index.tolist(), df['TA'].tolist(), df['SW'].tolist()]


def query_time_series_data() -> dict:

    res = dict()

    objects = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix='csv')

    for obj in objects:
        dropdown_mappers = []

        try:
            key = obj.get('Key')
            site_name = str(key).split("/")[1].capitalize()
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

            return res
        except Exception as err:
            print(f"error retrieving object: {err}")
            continue


def read_time_series_data():
    return


if __name__ == "__main__":
    # read_csv()
    query_time_series_data()