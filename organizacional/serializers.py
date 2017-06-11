from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models


class EmpleadoSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo empleado."""

    class Meta:
        model = models.Empleado
        fields = SelectableSerializerMixin.mixin_fields