from rest_framework import serializers
from . import models


class HorarioAtencionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo HorarioAtencion."""

    class Meta:
        model = models.HorarioAtencion
        fields = ['id', 'title', 'start', 'end', 'medico', 'sucursal']