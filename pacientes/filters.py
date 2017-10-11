import django_filters
from . import models

class SesionFilter(django_filters.FilterSet):
    """Filtro para las sesiones."""

    fecha = django_filters.DateFilter(lookup_expr='contains')

    class Meta:
        model = models.Sesion
        fields = ['estado', 'fecha']