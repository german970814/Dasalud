from django.db import transaction
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from pacientes.models import Paciente, Orden
from . import models


class HorarioAtencionSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo HorarioAtencion."""

    class Meta:
        model = models.HorarioAtencion
        fields = ['id', 'title', 'start', 'end', 'medico', 'sucursal']

class PersonaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Persona."""

    class Meta:
        model = models.Persona
        fields = ['id', 'numero_documento', 'tipo_documento', 'nombres', 'apellidos', 'telefono', 'celular', 'direccion']


class CitaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Cita."""

    end = serializers.DateTimeField(source='horario.end', read_only=True)
    title = serializers.CharField(source='paciente.__str__', read_only=True)
    start = serializers.DateTimeField(source='horario.start', read_only=True)
    redirecciona = serializers.BooleanField(source='cumplida', read_only=True)
    edit_link = serializers.HyperlinkedIdentityField(view_name='agenda:citas-detail')
    redirecciona_link = serializers.SerializerMethodField()

    class Meta:
        model = models.Cita
        fields = [
            'id', 'paciente', 'servicio', 'estado', 'horario', 'start', 'end', 'title', 'redirecciona',
            'redirecciona_link', 'edit_link', 'sesion'
        ]
    
    expandable_fields = {
        'paciente': (PersonaSerializer, {'source': 'paciente'})
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.fields['paciente'], PersonaSerializer):
            self.fields['paciente'].fields['numero_documento'].validators = []

    def create(self, validated_data):  #  TODO ver si se crea metodo en manager de Cita
        paciente_data = validated_data.pop('paciente')

        with transaction.atomic():
            documento = paciente_data.pop('numero_documento')
            paciente, _ = models.Persona.objects.get_or_create(numero_documento=documento, defaults=paciente_data)
            validated_data.update({'paciente': paciente})
            return super().create(validated_data)
    
    def update(self, instance, validated_data):  #  TODO ver si se crea metodo en manager de Cita
        paciente_data = validated_data.pop('paciente')
        paciente = instance.paciente

        with transaction.atomic():
            paciente.update(**paciente_data)
            instance.update(**validated_data)
        
        return instance
    
    def get_redirecciona_link(self, obj):
        if not obj.cumplida:
            return None
        
        request = self.context.get('request', None)
        if not obj.sesion:
            try:
                paciente = Paciente.objects.get(numero_documento=obj.paciente.numero_documento)
                return reverse('pacientes:ordenes-nueva', args=(paciente.id,), request=request)
            except Exception as e:
                return reverse('pacientes:crear', request=request)
        else:
            orden = Orden.objects.get(servicios_realizar__sesiones=obj.sesion_id)
            return reverse('pacientes:ordenes-detalle', kwargs={'paciente': orden.paciente_id, 'pk': orden.pk}, request=request)

