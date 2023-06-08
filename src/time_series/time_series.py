import pandas as pd

from constants.constants import MINIO_BUCKET
from utils.minio import Minio_Object


def read_csv():
    df = pd.read_csv('/Users/tripham/Desktop/satellite-dynamic-report/src/data/csv/Housel_DD_Input.csv', index_col='Date')

    # print(df.index.tolist())
    #
    # print(df['TA'].tolist())

    # print(df)

    return [df.index.tolist(), df['TA'].tolist(), df['SW'].tolist()]


def query_time_series_data():
    objects = Minio_Object.minio_list_objects(MINIO_BUCKET, prefix='csv')

    print(objects)

    for obj in objects:
        print(obj.get('Key'))




    # raw = Minio_Object.minio_get("/shapefile/housel/Housel_v2.shp")

def read_time_series_data():
    return


if __name__ == "__main__":
    # read_csv()
    read_time_series_data()