"""Thin wrapper around SSM Parameter Store."""

import boto3


class ParameterClient:
    """Reads encrypted parameters."""

    def __init__(self) -> None:
        self._client = boto3.client("ssm")

    def get_secret(self, name: str) -> str:
        """Return the decrypted value of a SecureString parameter."""
        return self._client.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
