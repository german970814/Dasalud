import datetime
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework import serializers
from common.serializers import PrefixFieldSerializerNameMixin
from .models import Paciente, Orden, Acompanante


class PacienteSerializer(PrefixFieldSerializerNameMixin, serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    edit_link = serializers.HyperlinkedIdentityField(view_name='pacientes:editar')

    class Meta:
        model = Paciente
        fields = (
            'id', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'estado_civil', 
            'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email', 'grupo_sanguineo', 
            'grupo_etnico', 'profesion', 'activo', 'fecha_ingreso', 'edit_link'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = Paciente.URBANO
        self.fields['grupo_etnico'].initial = Paciente.OTRO

class OrdenSerializer(PrefixFieldSerializerNameMixin, serializers.ModelSerializer):
    """Serializer para el modelo orden."""

    class Meta:
        model = Orden
        fields = ('autorizacion', 'pendiente_autorizacion', 'empresa', 'afiliacion', 'tipo_usuario', 'forma_pago')

class AcompananteSerializer(PrefixFieldSerializerNameMixin, serializers.ModelSerializer):
    """Serializer para el modelo acompanante."""

    class Meta:
        model = Acompanante
        fields = ('asistio', 'nombre', 'direccion', 'telefono')
