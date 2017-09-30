import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from common.schema import BaseNode
from . import models
from .filters import CitaFilter


class Agenda(DjangoObjectType):

    duracion = graphene.String()

    class Meta:
        model = models.Agenda
        description = 'Agendas que maneja el cliente'
        interfaces = (BaseNode,)
    
    def resolve_duracion(self, args, context, info):
        return str(self.duracion)


class HorarioAtencion(DjangoObjectType):

    class Meta:
        model = models.HorarioAtencion
        interfaces = (BaseNode,)


class Persona(DjangoObjectType):

    nombre_completo = graphene.String(source='__str__')

    class Meta:
        model = models.Persona
        interfaces = (BaseNode,)


class Cita(DjangoObjectType):

    start = graphene.types.datetime.DateTime(source='start')
    end = graphene.types.datetime.DateTime(source='end')
    title = graphene.String()
    
    class Meta:
        model = models.Cita
        filter_fields = ['estado']
        interfaces = (BaseNode,)
    
    def resolve_title(self, args, context, info):
        return str(self.paciente)


class Query(graphene.AbstractType):
    cita = BaseNode.Field(Cita)
    citas = DjangoFilterConnectionField(Cita, filterset_class=CitaFilter, description='Todas las citas')
    agendas = DjangoConnectionField(Agenda, description='Todas las agendas')
