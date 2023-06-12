# satellite-dynamic-report
**Pilot run for dynamic climate report for Texas and Oklahoma**

## I. Installation
1. Activate the environment from the terminal/command line
    ```shell
    conda activate satellite-dynamic-report
    ```

2. Install the required packages
    ```shell
    pip install -r requirements.txt
    ```

## II. Data Organization
- Satellite data is stored in MinIO. The organization format is as follows:
    ```shell
    └── Bucket-Name (dynamic-data)
        ├── shapefile
        │   ├── housel
        │   │   └── housel.shp
        │   ├── pratt
        │   │   └── pratt.shp
        │   └── weisse
        │       └── weisse.shp
        │      
        ├── evi
        │   ├── housel
        │   │   ├── yyyy-mm-dd.tif
        │   │   ├── yyyy-mm-dd.tif
        │   │   └── yyyy-mm-dd.tif
        │   ├── pratt
        │   │   ├── yyyy-mm-dd.tif
        │   │   └── yyyy-mm-dd.tif
        │   └── weisse
        │       ├── yyyy-mm-dd.tif
        │       ├── yyyy-mm-dd.tif
        │       └── yyyy-mm-dd.tif
        └── sr
            ├── housel
            │   ├── yyyy-mm-dd.tif
            │   ├── yyyy-mm-dd.tif
            │   └── yyyy-mm-dd.tif
            ├── pratt
            │   ├── yyyy-mm-dd.tif
            │   └── yyyy-mm-dd.tif
            └── weisse
                ├── yyyy-mm-dd.tif
                ├── yyyy-mm-dd.tif
                └── yyyy-mm-dd.tif
    ```
- Different types of data must be organized into separate directories
  - For example, if we have NDVI and EV data, they should be in 2 separate directories
  - If we have 2 sites with available NDVI data, we must organize the NDVI by site name
- File names of the GeoTiff must be of format yyyy-mm-dd.tif (e.g. 2023-06-01.tiff) 
- The name of the directories must be of lowercase, without space between each word of the directory name

## III. Running the app
The app is run on port 18050