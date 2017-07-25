import django_filters
from django_filters import rest_framework as filters
from organizacional.models import Sucursal, Empleado
from . import models

class CitaFilter(filters.FilterSet):
    """Filtro para la citas por medico y sucursal."""

    medico = django_filters.ModelChoiceFilter(name='horario__medico', queryset=Empleado.objects.medicos())
    sucursal = django_filters.ModelChoiceFilter(name='horario__sucursal', queryset=Sucursal.objects.all())

    class Meta:
        model = models.Cita
        fields = ['medico', 'sucursal']

