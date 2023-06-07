import geopandas
import os


def shapefile_to_geojson(file_path: str):
    dir_path = os.path.dirname(file_path)
    f_name = os.path.basename(f_path)
    f_name_wo_ext = os.path.splitext(f_name)

    shp_file = geopandas.read_file(file_path)
    shp_file.to_file('myJson.geojson', driver='GeoJSON')


if __name__ == "__main__":
    f_path = "/Users/tripham/Documents/Sample_Data/1_shp_files_v2/Housel_v2.shp"
    file_name = os.path.basename(f_path)

    dir_name = os.path.dirname(f_path)
    file = os.path.splitext(file_name)

    print("file_name", file_name)
    print("dir_name", dir_name)
    print("file", file)

    print("/".join([dir_name, file[0] + ".geojson"]))
