import boto3
from botocore.exceptions import ClientError
from .config import settings


class AWSService(object):

    _s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    _bucket = _s3.Bucket(settings.AWS_S3_BUCKET_NAME)

    @classmethod
    def upload_file(cls, contents: bytes,  key: str) -> None:
        cls._bucket.put_object(Key=key, Body=contents)

    @classmethod
    def download_file(cls,  key: str) -> bytes:
        try:
            return cls._s3.Object(bucket_name=settings.AWS_S3_BUCKET_NAME, key=key).get()['Body'].read()
        except ClientError as e:
            print(e)
