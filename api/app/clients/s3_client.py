"""Thin wrapper around S3."""

import boto3
from botocore.exceptions import ClientError

MISSING_OBJECT_CODE = "NoSuchKey"


class ObjectClient:
    """Reads text files from S3."""

    def __init__(self) -> None:
        self._client = boto3.client("s3")

    def get_text(self, bucket: str, key: str) -> str | None:
        """Return the file's text, or None when the file doesn't exist."""
        try:
            response = self._client.get_object(Bucket=bucket, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] == MISSING_OBJECT_CODE:
                return None
            raise
        return response["Body"].read().decode("utf-8")
