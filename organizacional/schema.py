import graphene
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField, filterset
from common.schema import BaseNode
from .filters import EmpleadoFilter
from . import models


class Sucursal(DjangoObjectType):

    class Meta:
        model = models.Sucursal
        interfaces = (BaseNode,)


class Institucion(DjangoObjectType):

    class Meta:
        model = models.Institucion
        interfaces = (BaseNode,)


class Empleado(DjangoObjectType):

    nombre_completo = graphene.String(source='__str__')
    instituciones = DjangoFilterConnectionField(Institucion)

    class Meta:
        model = models.Empleado
        interfaces = (BaseNode,)
        filter_fields = ['instituciones']


class Query(graphene.AbstractType):
    medicos = DjangoFilterConnectionField(Empleado, description='Todos los medicos')
    instituciones = DjangoConnectionField(Institucion, description='Todas las instituciones')
    sucursales = DjangoConnectionField(Sucursal, description='Todas las sucursales')

    def resolve_medicos(self, args, context, info):
        qs = models.Empleado.objects.medicos()
        if 'instituciones' in args:
            qs = qs.distinct()  # se aplica distinct para que no tire error cuando se usa aplica el filtro
        
        return qs
