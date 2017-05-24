from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    class Meta:
        model = Paciente
        fields = (
            'id', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'estado_civil', 
            'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email', 'grupo_sanguineo', 
            'grupo_etnico', 'activo'
        )
