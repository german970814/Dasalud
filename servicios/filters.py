import django_filters
from .models import Plan

class PlanFilter(django_filters.FilterSet):
    """Filtro para el modelo plan."""

    institucion = django_filters.NumberFilter(name='cliente__instituciones')

    class Meta:
        model = Plan
        fields = ['nombre']