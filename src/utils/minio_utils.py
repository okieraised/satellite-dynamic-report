import os
import datetime
import minio

import base64


class MinioUtils:
    @staticmethod
    def saveBase64Image(base64_image, root_folder=None):
        if base64_image is None:
            return None
        extension = '.jpg'
        try:
            imgdata = base64.b64decode(base64_image.split(',')[1])
        except:
            imgdata = base64.b64decode(base64_image)
        now = datetime.datetime.now()
        if not root_folder:
            root_folder = settings.MINIO['root_dossier']
        middle_name = root_folder + \
                      "/{}/{}/{}/".format(now.year, now.month, now.day)
        filename = "{}{}{}{}".format(
            now.hour, now.minute, now.second, now.microsecond)
        tmp_path = os.path.join(middle_name, filename + extension)

        MinioUtil.putObject(tmp_path, imgdata)
        return tmp_path

    @staticmethod
    def saveByteImage(b_imgdata, root_folder=None):
        if b_imgdata is None:
            return None
        if not root_folder:
            root_folder = settings.MINIO['root_dossier']

        now = datetime.datetime.now()
        middle_name = root_folder + \
                      "/{}/{}/{}/".format(now.year, now.month, now.day)
        filename = "{}{}{}{}".format(
            now.hour, now.minute, now.second, now.microsecond)
        tmp_path = os.path.join(middle_name, filename + 'jpg')

        MinioUtil.putObject(tmp_path, b_imgdata)
        return tmp_path

    @staticmethod
    def save_log_file(log_data, object_name="camera_unknown", bucket_name="logs", format="zip"):
        now = datetime.datetime.now()
        middle_name = "{}/{}/{}/{}".format(now.year, now.month, now.day, object_name)
        filename = "{}{}{}{}".format(
            now.hour, now.minute, now.second, now.microsecond)
        tmp_path = os.path.join(middle_name, filename + "." + format)
        MinioUtil.put_object_2(bucket_name=bucket_name,
                               object_new=tmp_path,
                               object_source=log_data)
        return tmp_path

    @staticmethod
    def get_base64_from_minio(path):
        avatar = minio.Minio_Object.get_opencv_img(path)
        if avatar is None:
            return None
        _, buffer = cv2.imencode('.jpg', avatar)
        avatar_base64 = base64.b64encode(buffer)
        return avatar_base64

    @staticmethod
    def get_url_from_minio_path(path):
        return "{}/{}".format(MINIO_PUBLIC_ENDPOINT_URL, path)

    @staticmethod
    def get_url_from_minio_bucket_path(bucket_name, path):
        return f"{MINIO_ENDPOINT_URL}/{bucket_name}/{path}"