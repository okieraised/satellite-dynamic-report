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

        self.s3_object = boto3.client('s3', endpoint_url=MINIO_ENDPOINT_URL, aws_access_key_id=MINIO_ACCESS_KEY_ID,
                                      aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
                                      config=Config(
                                          signature_version=MINIO_SIGNATURE_VERSION),
                                      region_name=MINIO_REGION_NAME)

        self.s3_file = boto3.resource('s3',
                                      endpoint_url=MINIO_ENDPOINT_URL,
                                      aws_access_key_id=MINIO_ACCESS_KEY_ID,
                                      aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
                                      config=Config(
                                          signature_version=MINIO_SIGNATURE_VERSION),
                                      region_name=MINIO_REGION_NAME)

    def put(self, buf, minio_path):
        try:
            self.s3_object.put_object(
                Bucket=MINIO_BUCKET, Key=minio_path, Body=buf)

        except:
            return False

    def minio_put(self, buf, minio_path):
        '''
        If bucket is not existed then create it first
        '''
        try:
            try:
                self.s3_object.head_bucket(Bucket=setting.bucket)
            except ClientError:
                print('bucket %s not exists, create the new one' % setting.bucket)
                self.s3_object.create_bucket(Bucket=MINIO_BUCKET)
        except Exception as err:
            print('could not create or read %s bucket' % setting.bucket)
            raise err

        try:
            print('putting file object %s in to bucket %s ' %
                  (minio_path, setting.bucket))
            self.s3_object.put_object(
                Bucket=setting.bucket, Key=minio_path, Body=buf)
        except Exception as err:
            print('put file object error')
            raise err

    def minio_get(self, minio_path):
        try:
            response = self.s3_object.get_object(
                Bucket=setting.bucket, Key=minio_path)
            return response['Body'].read()
        except Exception as err:
            print(err)
            return False

    def minio_upload(self, file_path, minio_path):
        try:
            self.s3_file.Bucket(setting.bucket).upload_file(
                file_path, minio_path)
        except Exception as err:
            print(err)
            return False

    def minio_download(self, minio_path, file_path):
        try:
            self.s3_file.Bucket(setting.bucket).download_file(
                minio_path, file_path)
        except Exception as err:
            print(err)
            return False


Minio_Object = Minio()
