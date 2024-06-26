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

3. Change the variables in the `.env` file to your S3 settings, but keeps the 
`MAPBOX_API_KEY` value the same

## II. Data Organization
- Satellite data is stored in MinIO. The organization format is as follows:
    ```shell
    └── Bucket-Name (dynamic-data)
        ├── shapefile
        │   ├── housel
        │   │   └── housel.geojson
        │   ├── pratt
        │   │   └── pratt.geojson
        │   └── weisse
        │       └── weisse.geojson
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
- Due to constraints in current mapping library, a custom access policy must be set for the MinIO bucket, 
paste this into the `Access Policy` section with `custom` option specified:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::dynamic-data"
            ]
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::dynamic-data/*"
            ]
        }
    ]
}
```

## III. Running the app
For local run, use pycharm and run the `app.py` file. The app is run on port 18050