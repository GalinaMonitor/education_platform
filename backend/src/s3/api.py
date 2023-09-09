import io
from typing import NoReturn

import boto3
from botocore.client import Config

from src.settings import settings


class AWSClient:
    def __init__(self):
        self.session = boto3.client(
            "s3",
            endpoint_url=settings.aws_host,
            region_name="ru-1",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(s3={"addressing_style": "path"}),
        )
        self.bucket_name = settings.aws_bucket_name

    def upload_file(self, file_io: io.BytesIO, filename: str) -> NoReturn:
        self.session.upload_fileobj(file_io, Bucket=self.bucket_name, Key=filename)

    def download_file(self, filename: str) -> io.BytesIO:
        file_io = io.BytesIO()
        self.session.download_fileobj(self.bucket_name, filename, file_io)
        file_io.seek(0)
        return file_io

    def delete_file(self, filename: str) -> NoReturn:
        self.session.delete_object(Bucket=self.bucket_name, Key=filename)
