import io

import boto3
from botocore.client import Config

from settings import settings


class AWSClient:
    def __init__(self):
        self.session = boto3.client(
            's3',
            endpoint_url=settings.aws_host,
            region_name='ru-1',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(s3={'addressing_style': 'path'})
        )
        self.bucket_name = settings.aws_bucket_name

    def upload_file(self, file_io: io.BytesIO, filename: str):
        self.session.upload_fileobj(
            file_io, Bucket=self.bucket_name, Key=filename
        )

    def download_file(self, filename: str):
        file_io = io.BytesIO()
        self.session.download_fileobj(self.bucket_name, filename, file_io)
        file_io.seek(0)
        return file_io

    def delete_file(self, filename: str):
        self.session.delete_object(Bucket=self.bucket_name, Key=filename)
