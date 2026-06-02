from functools import lru_cache
from typing import Any

import boto3
from botocore.client import Config
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from app.config import (
    S3_ACCESS_KEY,
    S3_BUCKET,
    S3_ENDPOINT_URL,
    S3_REGION,
    S3_SECRET_KEY,
)


@lru_cache
def _client() -> BaseClient:
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION,
        config=Config(signature_version="s3v4"),
    )


def ensure_bucket() -> None:
    client = _client()
    try:
        client.head_bucket(Bucket=S3_BUCKET)
    except ClientError:
        client.create_bucket(Bucket=S3_BUCKET)


def upload_bytes(key: str, data: bytes, content_type: str | None = None) -> str:
    extra: dict[str, Any] = {}
    if content_type:
        extra["ContentType"] = content_type
    _client().put_object(Bucket=S3_BUCKET, Key=key, Body=data, **extra)
    return key


def download_bytes(key: str) -> bytes:
    response: dict[str, Any] = _client().get_object(Bucket=S3_BUCKET, Key=key)  # type: ignore[assignment]
    body = response["Body"]
    return body.read()


def delete_object(key: str) -> None:
    try:
        _client().delete_object(Bucket=S3_BUCKET, Key=key)
    except ClientError:
        pass
