import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from . import models
from .filters import CitaFilter


class HorarioAtencion(DjangoObjectType):

    class Meta:
        model = models.HorarioAtencion
        interfaces = (graphene.Node,)


class Persona(DjangoObjectType):

    class Meta:
        model = models.Persona
        interfaces = (graphene.Node,)


class Cita(DjangoObjectType):

    start = graphene.types.datetime.DateTime(source='start')
    end = graphene.types.datetime.DateTime(source='end')
    
    class Meta:
        model = models.Cita
        filter_fields = ['estado']
        interfaces = (graphene.Node,)


class Query(graphene.AbstractType):
    citas = DjangoFilterConnectionField(Cita, filterset_class=CitaFilter, description='Todas las citas')

    def resolve_citas(self, args, context, info):
        return models.Cita.objects.all()