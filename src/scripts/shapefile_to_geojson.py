import geopandas
import os

from utils.file import list_file_with_same_ext


def shapefile_to_geojson(file_path: str):
    try:
        dir_name = os.path.dirname(file_path)
        f_name = os.path.basename(file_path)
        f_name_wo_ext = os.path.splitext(f_name)
        geojson_f_path = "/".join([dir_name, f_name_wo_ext[0] + ".geojson"])
        shp_file = geopandas.read_file(file_path)
        shp_file.to_file(geojson_f_path, driver='GeoJSON')
        return True

    except Exception as err:
        print(err)
        return False


if __name__ == "__main__":
    res = list_file_with_same_ext("/Users/tripham/Downloads/Sesajal_Data/shp", ".shp")
    for f in res:
        shapefile_to_geojson(f)

