import django_filters
from django_filters import rest_framework as filters
from organizacional.models import Sucursal, Empleado
from . import models

class CitaFilter(filters.FilterSet):
    """Filtro para la citas."""

    medico = django_filters.ModelChoiceFilter(name='horario__medico', queryset=Empleado.objects.medicos())
    sucursal = django_filters.ModelChoiceFilter(name='horario__sucursal', queryset=Sucursal.objects.all())
    documento_paciente = django_filters.CharFilter(name='paciente__numero_documento')
    fecha_inicial = django_filters.DateFilter(name='horario__start', lookup_expr='gte')
    no_asociada_orden = django_filters.BooleanFilter(name='sesion', lookup_expr='isnull')

    class Meta:
        model = models.Cita
        fields = ['medico', 'sucursal', 'documento_paciente', 'fecha_inicial', 'no_asociada_orden']

