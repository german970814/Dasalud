from rest_framework import serializers
from common.schema import BaseNode


class GlobalIDField(serializers.Field):
    """Global ID."""

    def to_internal_value(self, data):
        _, _id = BaseNode.from_global_id(data)
        return _id


