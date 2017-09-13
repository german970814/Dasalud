from rest_framework import serializers
from rest_framework.reverse import reverse
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
    url_adjunto = serializers.SerializerMethodField()

    class Meta:
        model = models.Historia
        fields = ['id', 'nombre_servicio', 'terminada', 'contenido', 'url_adjunto']
    
    def get_nombre_servicio(self, obj):
        return obj.sesion.servicio.servicio.nombre

    def get_url_adjunto(self, obj):
        return reverse('historias:adjuntos', args=(obj.sesion_id, ))


class AdjuntoSerializer(FlexFieldsModelSerializer):
    """"Serializer para el modelo Adjunto."""

    nombre = serializers.SerializerMethodField()
    url_delete = serializers.SerializerMethodField()

    class Meta:
        model = models.Adjunto
        fields = ['id', 'archivo', 'nombre', 'url_delete']
    
    def get_nombre(self, obj):
        split_name = obj.archivo.name.split('/')
        return split_name[-1]

    def get_url_delete(self, obj):
        return reverse('historias:adjuntos-eliminar', args=(obj.id, ))
