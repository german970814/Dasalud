from rest_framework import serializers
from common.serializers import SelectableSerializerMixin
from . import models


class EmpresaSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo empresa."""

    class Meta:
        model = models.Empresa
        fields = SelectableSerializerMixin.mixin_fields


class PlanSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para el modelo plan."""

    class Meta:
        model = models.Plan
        fields = SelectableSerializerMixin.mixin_fields


class TarifaServiciosEmpresaSerializer(SelectableSerializerMixin, serializers.ModelSerializer):
    """Serializer para """

    class Meta:
        model = models.TarifaServicio
        fields = SelectableSerializerMixin.mixin_fields + ['valor']
    
    def get_label(self, obj):
        return str(obj.servicio)
    
    def get_value(self, obj):
        return obj.servicio.pk
