from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from . import models


class FormatoSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Formato."""

    class Meta:
        model = models.Formato
        fields = ['id', 'nombre', 'contenido']


class HistoriaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Historia."""

    adjuntos_link = serializers.HyperlinkedIdentityField(
        view_name='historias:adjuntos', lookup_field='servicio_orden_id', lookup_url_kwarg='servicio'
    )

    class Meta:
        model = models.Historia
        fields = ['id', 'servicio_orden', 'terminada', 'adjuntos_link', 'contenido']


class AdjuntoSerializer(FlexFieldsModelSerializer):
    """"Serializer para el modelo Adjunto."""

    class Meta:
        model = models.Adjunto
        fields = ['id', 'archivo']
