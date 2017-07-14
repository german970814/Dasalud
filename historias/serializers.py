from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from . import models


class FormatoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Formato."""

    class Meta:
        model = models.Formato
        fields = ['id', 'nombre', 'contenido']


class HistoriaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Historia."""

    class Meta:
        model = models.Historia
        fields = ['id', 'servicio_orden', 'contenido', 'terminada']
