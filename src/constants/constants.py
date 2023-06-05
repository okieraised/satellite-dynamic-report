import os
import datetime

today = datetime.date.today()
year = today.year

YEARS = list(range(2003, year+1))


MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

OK_LAT = 35.481918
OK_LONG = -97.508469


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

