import django_filters
from graphene_django.filter import filterset
from django_filters import rest_framework as filters
from organizacional.models import Sucursal, Empleado
from . import models


class HorarioAtencionFilter(django_filters.FilterSet):
    """Filtro para los horarios de atención."""

    agenda = filterset.GlobalIDFilter(name='medico__agenda')

    class Meta:
        model = models.HorarioAtencion
        fields = ['agenda', 'sucursal']


class CitaFilter(filters.FilterSet):
    """Filtro para la citas."""

    sucursal = filterset.GlobalIDFilter(name='horario__sucursal')
    agenda = filterset.GlobalIDFilter(name='horario__medico__agenda')
    medico = django_filters.ModelChoiceFilter(name='horario__medico', queryset=Empleado.objects.medicos())
    documento_paciente = django_filters.CharFilter(name='paciente__numero_documento')
    fecha_inicial = django_filters.DateFilter(name='horario__start', lookup_expr='gte')
    no_asociada_orden = django_filters.BooleanFilter(name='sesion', lookup_expr='isnull')

    class Meta:
        model = models.Cita
        fields = ['agenda', 'medico', 'sucursal', 'documento_paciente', 'fecha_inicial', 'no_asociada_orden']
