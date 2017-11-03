import django_filters
from graphene_django.filter import filterset
from . import models


class HistoriaFilter(django_filters.FilterSet):

    paciente = filterset.GlobalIDFilter(name='sesion__servicio__orden__paciente')

    class Meta:
        model = models.Historia
        fields = ['paciente', 'terminada']
