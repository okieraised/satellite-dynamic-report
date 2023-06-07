import os
import datetime
from dotenv import load_dotenv


today = datetime.date.today()
year = today.year

YEARS = list(range(2003, year+1))

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")
MINIO_ENDPOINT_URL = os.getenv('MINIO_ENDPOINT_URL')
MINIO_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_SIGNATURE_VERSION = os.getenv('MINIO_SIGNATURE_VERSION')
MINIO_REGION_NAME = os.getenv('MINIO_REGION_NAME')
MINIO_BUCKET = os.getenv('MINIO_BUCKET')
MINIO_PUBLIC_ENDPOINT_URL = os.getenv('MINIO_PUBLIC_ENDPOINT_URL', '')

OK_LAT = 35.481918
OK_LONG = -97.508469

OH_LAT = 40.367474
OH_LONG = -82.996216


class MapType(object):
    OUTDOORS = "outdoors"
    OPEN_STREET_MAP = "open-street-map"
    SATELLITE = "satellite"
    DEFAULT = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


class DropdownMapper(object):
    WorldMap = [
        {
            "label": "Default",
            "value": MapType.DEFAULT,
        },
        {
            "label": "Open Street Map",
            "value": MapType.OPEN_STREET_MAP,
        },
        {
            "label": "Satellite",
            "value": MapType.SATELLITE,
        },
        {
            "label": "Outdoors",
            "value": MapType.OUTDOORS,
        },
    ]

    SatelliteData = [
        {
            "label": "Enhanced Vegetation Index (EVI)",
            "value": "EVI",
        },
        {
            "label": "Vegetation Index (VI)",
            "value": "VI",
        },
        {
            "label": "Surface Reflectance (SR)",
            "value": "SR",
        },
    ]

    WeekNumber = [{"label": f"Week {i}", "value": i} for i in list(range(1, 53))]

