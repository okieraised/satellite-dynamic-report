import os
import datetime
from dotenv import load_dotenv


today = datetime.date.today()
CURRENT_YEAR = today.year

YEARS = list(range(2003, CURRENT_YEAR + 1))

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

DEFAULT_CRS = "EPSG:4326"


class Site(object):
    Housel = "Housel"
    Pratt = "Pratt"
    Weisse = "Weisse"


class DataType(object):
    EVI = "EVI"
    VI = "VI"
    SR = "SR"


class MapType(object):
    OUTDOORS = "mapbox/outdoors-v12"
    SATELLITE = "mapbox/satellite-v9"
    SATELLITE_STREET = "mapbox/satellite-streets-v12"
    MAPBOX_STREET = "mapbox/streets-v12"
    NAVIGATION_DAY = "mapbox/navigation-day-v1"
    NAVIGATION_NIGHT = "mapbox/navigation-night-v1"
    DEFAULT = "plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


BASEMAP_URL = "https://api.mapbox.com/styles/v1/{map_style}/tiles/{{z}}/{{x}}/{{y}}?access_token={access_token}"

DEFAULT_SITE = Site.Housel
DEFAULT_DATA = DataType.EVI


class DropdownMapper(object):
    WorldMap = [
        {
            "label": "Default",
            "value": MapType.DEFAULT,
        },
        {
            "label": "Street",
            "value": MapType.MAPBOX_STREET,
        },
        {
            "label": "Satellite",
            "value": MapType.SATELLITE,
        },
        {
            "label": "Outdoors",
            "value": MapType.OUTDOORS,
        },
        {
            "label": "Navigation (Day)",
            "value": MapType.NAVIGATION_DAY,
        },
        {
            "label": "Navigation (Night)",
            "value": MapType.NAVIGATION_NIGHT,
        },
    ]

    SatelliteData = [
        {
            "label": "Enhanced Vegetation Index (EVI)",
            "value": DataType.EVI,
        },
        {
            "label": "Vegetation Index (VI)",
            "value": DataType.VI,
        },
        {
            "label": "Surface Reflectance (SR)",
            "value": DataType.SR,
        },
    ]

    WeekNumber = [{"label": f"Week {i}", "value": i} for i in list(range(1, 54))]

    SiteName = [{"label": val, "value": val} for key, val in Site.__dict__.items() if not key.startswith('__')]


if __name__ == "__main__":
    x = [{"label": val, "value": val} for key, val in Site.__dict__.items() if not key.startswith('__')]
