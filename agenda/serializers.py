from django.db import transaction
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
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
        fields = ['id', 'numero_documento', 'tipo_documento', 'nombres', 'apellidos', 'telefono', 'celular']


class CitaSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Cita."""

    title = serializers.CharField(source='paciente.__str__', read_only=True)
    start = serializers.DateTimeField(source='horario.start', read_only=True)
    end = serializers.DateTimeField(source='horario.end', read_only=True)

    class Meta:
        model = models.Cita
        fields = ['id', 'paciente', 'servicio', 'estado', 'horario', 'start', 'end', 'title']
    
    expandable_fields = {
        'paciente': (PersonaSerializer, {'source': 'paciente'})
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.fields['paciente'], PersonaSerializer):
            print(self.fields['paciente'].fields['numero_documento'])
            self.fields['paciente'].fields['numero_documento'].validators = []

    def create(self, validated_data):  #  TODO ver si se crea metodo en manager de Cita
        paciente_data = validated_data.pop('paciente')

        with transaction.atomic():
            documento = paciente_data.pop('numero_documento')
            paciente, _ = models.Persona.objects.get_or_create(numero_documento=documento, defaults=paciente_data)
            validated_data.update({'paciente': paciente})
            return super().create(validated_data)


