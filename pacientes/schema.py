import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from common.schema import BaseNode

from . import models


class Paciente(DjangoObjectType):

    class Meta:
        model = models.Paciente
        interfaces = (BaseNode,)


class Orden(DjangoObjectType):

    class Meta:
        model = models.Orden
        interfaces = (BaseNode,)


class ServicioRealizar(DjangoObjectType):

    class Meta:
        model = models.ServicioRealizar
        interfaces = (BaseNode,)


class Sesion(DjangoObjectType):

    url_historia = graphene.String()

    class Meta:
        model = models.Sesion
        filter_fields = ['estado']
        interfaces = (BaseNode,)

    def resolve_url_historia(self, args, context, info):
        from django.core.urlresolvers import reverse
        return reverse('pacientes:historias', args=(self.id, ))


class Acompanante(DjangoObjectType):

    class Meta:
        model = models.Acompanante
        interfaces = (BaseNode,)


class Query(graphene.AbstractType):
    sesion = BaseNode.Field(Sesion)
    sesiones = DjangoFilterConnectionField(Sesion, description='Todas las sesiones')
    servicio_realizar = BaseNode.Field(ServicioRealizar)
    servicios_realizar = DjangoFilterConnectionField(ServicioRealizar, description='Todos los servicios a realizar')
    orden = BaseNode.Field(Orden)
    ordenes = DjangoFilterConnectionField(Orden, description='Todas las ordenes')
    paciente = BaseNode.Field(Paciente)
    pacientes = DjangoFilterConnectionField(Paciente, description='Todas las ordenes')
