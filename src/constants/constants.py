import os

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

OK_LAT = 35.481918
OK_LONG = -97.508469


class MapType(object):
    OUTDOOR = "outdoors"
    OEN_STREET_MAP = "open-street-map"
    SATELLITE = "satellite"

