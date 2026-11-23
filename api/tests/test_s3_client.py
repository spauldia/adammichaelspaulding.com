from collections.abc import Iterator

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws

from app.clients.s3_client import ObjectClient

BUCKET = "site-chat-notes-test"


@pytest.fixture
def s3() -> Iterator[None]:
    with mock_aws():
        boto3.client("s3").create_bucket(Bucket=BUCKET)
        yield


def test_returns_the_file_text(s3: None) -> None:
    boto3.client("s3").put_object(Bucket=BUCKET, Key="notes.md", Body=b"## Hobbies\n- Chess\n")

    assert ObjectClient().get_text(BUCKET, "notes.md") == "## Hobbies\n- Chess\n"


def test_missing_file_returns_none(s3: None) -> None:
    assert ObjectClient().get_text(BUCKET, "notes.md") is None


def test_missing_bucket_raises(s3: None) -> None:
    with pytest.raises(ClientError):
        ObjectClient().get_text("bucket-that-does-not-exist", "notes.md")
