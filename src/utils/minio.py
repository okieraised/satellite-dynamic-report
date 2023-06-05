import os
import boto3

from botocore.client import Config
from botocore.exceptions import ClientError

MINIO_ENDPOINT_URL = os.getenv('MINIO_ENDPOINT_URL')
MINIO_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_SIGNATURE_VERSION = os.getenv('MINIO_SIGNATURE_VERSION')
MINIO_REGION_NAME = os.getenv('MINIO_REGION_NAME')
MINIO_BUCKET = os.getenv('MINIO_BUCKET')
MINIO_PUBLIC_ENDPOINT_URL = os.getenv('MINIO_PUBLIC_ENDPOINT_URL', '')


class Minio:

    def __init__(self):

        self.s3_object = boto3.client('s3',
                                      endpoint_url=MINIO_ENDPOINT_URL,
                                      aws_access_key_id=MINIO_ACCESS_KEY_ID,
                                      aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
                                      config=Config(
                                          signature_version=MINIO_SIGNATURE_VERSION
                                      ),
                                      region_name=MINIO_REGION_NAME)

        self.s3_file = boto3.resource('s3',
                                      endpoint_url=MINIO_ENDPOINT_URL,
                                      aws_access_key_id=MINIO_ACCESS_KEY_ID,
                                      aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
                                      config=Config(
                                          signature_version=MINIO_SIGNATURE_VERSION
                                      ),
                                      region_name=MINIO_REGION_NAME)

    def put(self, buf, minio_path):
        try:
            self.s3_object.put_object(Bucket=MINIO_BUCKET, Key=minio_path, Body=buf)
        except Exception as err:
            return err

    def minio_put(self, buf, minio_path):
        try:
            try:
                self.s3_object.head_bucket(Bucket=MINIO_BUCKET)
            except ClientError:
                print(f'bucket {MINIO_BUCKET} not exists, create the new one')
                self.s3_object.create_bucket(Bucket=MINIO_BUCKET)
        except Exception as err:
            print(f'could not create or read {MINIO_BUCKET} bucket')
            raise err

        try:
            print(f'putting file object {minio_path} in to bucket {MINIO_BUCKET}')
            self.s3_object.put_object(Bucket=MINIO_BUCKET, Key=minio_path, Body=buf)
        except Exception as err:
            print('put file object error')
            raise err

    def minio_get(self, minio_path):
        try:
            response = self.s3_object.get_object(Bucket=MINIO_BUCKET, Key=minio_path)
            return response['Body'].read()
        except Exception as err:
            print(err)
            return False

    def minio_upload(self, file_path, minio_path):
        try:
            self.s3_file.Bucket(MINIO_BUCKET).upload_file(file_path, minio_path)
        except Exception as err:
            print(err)
            return False

    def minio_download(self, minio_path, file_path):
        try:
            self.s3_file.Bucket(MINIO_BUCKET).download_file(minio_path, file_path)
        except Exception as err:
            print(err)
            return False


Minio_Object = Minio()
