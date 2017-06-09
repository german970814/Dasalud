import datetime
from django.db import transaction
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework import serializers
from servicios.models import Servicio
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    edit_link = serializers.HyperlinkedIdentityField(view_name='pacientes:detalle')
    ordenes_link = serializers.HyperlinkedIdentityField(view_name='pacientes:ordenes')

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'estado_civil', 
            'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email', 'grupo_sanguineo', 
            'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia', 'activo', 'fecha_ingreso',
            'nombre_responsable', 'direccion_responsable', 'telefono_responsable' , 'edit_link', 'ordenes_link',
            'identificacion_padre', 'nombre_padre', 'identificacion_madre', 'nombre_madre'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = models.Paciente.URBANO
        self.fields['grupo_etnico'].initial = models.Paciente.OTRO

class OrdenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo orden."""

    class Meta:
        model = models.Orden
        fields = [
            'sucursal', 'autorizacion', 'pendiente_autorizacion', 'institucion', 'plan',
            'afiliacion', 'tipo_usuario', 'forma_pago'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['afiliacion'].initial = models.Orden.PARTICULAR
        self.fields['tipo_usuario'].initial = models.Orden.PARTICULAR

class ServicioOrdenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo servicio orden."""

    class Meta:
        model = models.ServicioOrden
        fields = ['medico', 'servicio', 'tipo_pago', 'valor', 'descuento']

class AcompananteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo acompanante."""

    class Meta:
        model = models.Acompanante
        fields = ['asistio', 'nombre', 'direccion', 'telefono']

class CrearOrdenSerializer(OrdenSerializer):
    """Serializer para la creación de una orden."""

    acompanante = AcompananteSerializer()
    servicios = ServicioOrdenSerializer(many=True, source='servicios_orden')

    class Meta(OrdenSerializer.Meta):
        fields = OrdenSerializer.Meta.fields + ['acompanante', 'servicios', 'paciente']
        read_only_fields = ['paciente']
    
    def create(self, validated_data):
        servicios_data = validated_data.pop('servicios_orden')
        acompanante_data = validated_data.pop('acompanante')

        with transaction.atomic():
            orden = super().create(validated_data)
            models.Acompanante.objects.create(orden=orden, **acompanante_data)
            for servicio_data in servicios_data:
                models.ServicioOrden.objects.create(orden=orden, **servicio_data)
            return orden
