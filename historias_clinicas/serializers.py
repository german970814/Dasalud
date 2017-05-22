from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    class Meta:
        model = Paciente
        fields = ('id', 'nombres', 'apellidos', 'numero_documento', 'genero')