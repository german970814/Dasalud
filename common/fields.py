from rest_framework import serializers
from common.schema import BaseNode


class GlobalIDField(serializers.Field):
    """Global ID."""

    def __init__(self, type_, *args, **kwargs):
        self.type_ = type_.capitalize()
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        _type, _id = BaseNode.from_global_id(data)
        return _id

    def to_representation(self, obj):
        return BaseNode.to_global_id(self.type_, obj)