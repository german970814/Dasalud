from rest_framework import serializers, relations
from .fields import GlobalIDField


class SelectableSerializerMixin(serializers.Serializer):
    """Mixin que le agrega campos label y value para ser usado en vaadin-combobox."""

    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    mixin_fields = ['label', 'value']

    def get_label(self, obj):
        return str(obj)
    
    def get_value(self, obj):
        return obj.pk


class PrimaryKeyGlobalIDMixin(serializers.Serializer):
    """Mixin para deserializar ForeingKey que usen global ID de graphql."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            if isinstance(field, relations.PrimaryKeyRelatedField):
                field.pk_field = GlobalIDField()
