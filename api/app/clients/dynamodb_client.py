"""Thin wrapper around the DynamoDB table."""

import boto3


class TableClient:
    """Reads and adds to number attributes in one DynamoDB table."""

    def __init__(self, table_name: str) -> None:
        self._table = boto3.resource("dynamodb").Table(table_name)

    def get_number(self, key: str, attribute: str) -> int:
        """Return the attribute's value, or 0 when the item does not exist."""
        item = self._table.get_item(Key={"pk": key}, ConsistentRead=True).get("Item", {})
        return int(item.get(attribute, 0))

    def add_number(self, key: str, attribute: str, amount: int, expires_at: int) -> int:
        """Add to the attribute and return its new value."""
        response = self._table.update_item(
            Key={"pk": key},
            UpdateExpression="SET expires_at = if_not_exists(expires_at, :expires_at) ADD #value :amount",
            ExpressionAttributeNames={"#value": attribute},
            ExpressionAttributeValues={":amount": amount, ":expires_at": expires_at},
            ReturnValues="UPDATED_NEW",
        )
        return int(response["Attributes"][attribute])
