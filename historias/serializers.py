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

    nombre_servicio = serializers.SerializerMethodField()
    adjuntos_link = serializers.HyperlinkedIdentityField(
        view_name='historias:adjuntos', lookup_field='sesion_id', lookup_url_kwarg='sesion'
    )

    class Meta:
        model = models.Historia
        fields = ['id', 'nombre_servicio', 'terminada', 'adjuntos_link', 'contenido']
    
    def get_nombre_servicio(self, obj):
        return obj.sesion.servicio.servicio.nombre


class AdjuntoSerializer(FlexFieldsModelSerializer):
    """"Serializer para el modelo Adjunto."""

    nombre = serializers.SerializerMethodField()

    class Meta:
        model = models.Adjunto
        fields = ['id', 'archivo', 'nombre']
    
    def get_nombre(self, obj):
        split_name = obj.archivo.name.split('/')
        return split_name[-1]
