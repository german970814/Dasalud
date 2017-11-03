import graphene
import django_filters

from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from django.core.urlresolvers import reverse
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
    can_delete = graphene.Boolean()

    class Meta:
        model = models.ServicioRealizar
        interfaces = (BaseNode,)
    
    def resolve_can_delete(self, args, context, info):
        return False


class Sesion(DjangoObjectType):

    pk = graphene.Int(source='pk')
    url_historia = graphene.String()
    estado_display = graphene.String(source='get_estado_display')
    can_edit = graphene.Boolean()
    terminada = graphene.Boolean(source='terminada')

    class Meta:
        model = models.Sesion
        interfaces = (BaseNode,)

    def resolve_url_historia(self, args, context, info):
        return reverse('pacientes:historias', args=(self.id, ))

    def resolve_can_edit(self, args, context, info):
        return True


class Acompanante(DjangoObjectType):

    class Meta:
        model = models.Acompanante
        interfaces = (BaseNode,)


class Query(graphene.AbstractType):
    sesion = BaseNode.Field(Sesion)
    sesiones = DjangoFilterConnectionField(Sesion, filterset_class=filters.SesionFilter,  description='Todas las sesiones')
    sesiones_con_triage = DjangoFilterConnectionField(Sesion, filterset_class=filters.SesionFilter, description='Sesiones que en la historia se les ingresa triage')
    servicio_realizar = BaseNode.Field(ServicioRealizar)
    servicios_realizar = DjangoFilterConnectionField(ServicioRealizar, description='Todos los servicios a realizar')
    orden = BaseNode.Field(Orden)
    ordenes = DjangoFilterConnectionField(Orden, description='Todas las ordenes')
    paciente = BaseNode.Field(Paciente)
    pacientes = DjangoFilterConnectionField(Paciente, description='Todas las ordenes')

    def resolve_sesiones(self, args, context, info):
        return models.Sesion.objects.filter(medico__usuario=context.user)

    def resolve_sesiones_con_triage(self, args, context, info):
        return models.Sesion.objects.filter(servicio__servicio__formato__triage=True)
