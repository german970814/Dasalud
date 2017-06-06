import datetime
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework import serializers
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    edit_link = serializers.HyperlinkedIdentityField(view_name='pacientes:editar')

    class Meta:
        model = models.Paciente
        fields = (
            'id', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'estado_civil', 
            'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email', 'grupo_sanguineo', 
            'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia', 'activo', 'fecha_ingreso',
            'nombre_responsable', 'direccion_responsable', 'telefono_responsable' , 'edit_link',
            'identificacion_padre', 'nombre_padre', 'identificacion_madre', 'nombre_madre' 
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = models.Paciente.URBANO
        self.fields['grupo_etnico'].initial = models.Paciente.OTRO

class OrdenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo orden."""

    class Meta:
        model = models.Orden
        fields = ('sucursal', 'autorizacion', 'pendiente_autorizacion', 'institucion', 'empresa', 'afiliacion', 'tipo_usuario', 'forma_pago')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['afiliacion'].initial = models.Orden.PARTICULAR
        self.fields['tipo_usuario'].initial = models.Orden.PARTICULAR

class ServicioOrdenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo servicio orden."""

    class Meta:
        model = models.ServicioOrden
        fields = ('medico', 'servicio', 'tipo_pago', 'valor', 'descuento')

class AcompananteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo acompanante."""

    class Meta:
        model = models.Acompanante
        fields = ('asistio', 'nombre', 'direccion', 'telefono')
