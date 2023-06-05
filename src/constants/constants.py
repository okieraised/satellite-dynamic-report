import os
import datetime

today = datetime.date.today()
year = today.year

YEARS = list(range(2003, year+1))


MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

OK_LAT = 35.481918
OK_LONG = -97.508469


class MapType(object):
    OUTDOOR = "outdoors"
    OEN_STREET_MAP = "open-street-map"
    SATELLITE = "satellite"
    DEFAULT = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"