import graphene
import django_filters
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from common.schema import BaseNode

from historias.schema import Historia
from . import models
from . import filters


class Paciente(DjangoObjectType):
    
    historias = DjangoConnectionField(Historia)

    class Meta:
        model = models.Paciente
        interfaces = (BaseNode,)

    def resolve_historias(self, args, context, info):
        return self.get_historias()


class Orden(DjangoObjectType):

    class Meta:
        model = models.Orden
        interfaces = (BaseNode,)


class ServicioRealizar(DjangoObjectType):

    pk = graphene.Int(source='pk')
    sesiones_cumplidas = graphene.Int(source='numero_sesiones_cumplidas', description='Número de sesiones cumplidas')

    class Meta:
        model = models.ServicioRealizar
        interfaces = (BaseNode,)


class Sesion(DjangoObjectType):

    pk = graphene.Int(source='pk')
    url_historia = graphene.String()
    estado_display = graphene.String(source='get_estado_display')

    class Meta:
        model = models.Sesion
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
    sesiones = DjangoFilterConnectionField(Sesion, filterset_class=filters.SesionFilter,  description='Todas las sesiones')
    servicio_realizar = BaseNode.Field(ServicioRealizar)
    servicios_realizar = DjangoFilterConnectionField(ServicioRealizar, description='Todos los servicios a realizar')
    orden = BaseNode.Field(Orden)
    ordenes = DjangoFilterConnectionField(Orden, description='Todas las ordenes')
    paciente = BaseNode.Field(Paciente)
    pacientes = DjangoFilterConnectionField(Paciente, description='Todas las ordenes')

    def resolve_sesiones(self, args, context, info):
        return models.Sesion.objects.filter(medico__usuario=context.user)
