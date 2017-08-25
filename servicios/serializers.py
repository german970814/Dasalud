from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models


class ClienteSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo cliente."""

    class Meta:
        model = models.Cliente
        fields = SelectableSerializerMixin.mixin_fields


class PlanSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo plan."""

    class Meta:
        model = models.Plan
        fields = SelectableSerializerMixin.mixin_fields


class TarifaClienteSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para las tarifas"""

    class Meta:
        model = models.Tarifa
        fields = SelectableSerializerMixin.mixin_fields + ['valor']
    
    def get_label(self, obj):
        return str(obj.servicio)
    
    def get_value(self, obj):
        return obj.servicio.pk
