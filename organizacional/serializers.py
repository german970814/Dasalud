from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models


class SucursalSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo Sucursal."""

    class Meta:
        model = models.Sucursal
        fields = SelectableSerializerMixin.mixin_fields


class EmpleadoSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo empleado."""

    class Meta:
        model = models.Empleado
        fields = SelectableSerializerMixin.mixin_fields + ['duracion_cita']