import graphene
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField, filterset
from common.schema import BaseNode
from . import models


class Sucursal(DjangoObjectType):

    pk = graphene.Int(source='pk')

    class Meta:
        model = models.Sucursal
        interfaces = (BaseNode,)


class Institucion(DjangoObjectType):

    class Meta:
        model = models.Institucion
        interfaces = (BaseNode,)


class Empleado(DjangoObjectType):

    pk = graphene.Int(source='pk')
    title = graphene.String(source='__str__')
    nombre_completo = graphene.String(source='__str__')
    instituciones = DjangoFilterConnectionField(Institucion)
    duracion = graphene.String(description='Duración de la atención de las citas.')

    class Meta:
        model = models.Empleado
        interfaces = (BaseNode,)
        filter_fields = ['instituciones', 'agenda', 'sucursal']
    
    def resolve_duracion(self, args, context, info):
        return str(self.duracion_cita or self.agenda.duracion)


class Query(graphene.AbstractType):
    medicos = DjangoFilterConnectionField(Empleado, description='Todos los medicos')
    instituciones = DjangoConnectionField(Institucion, description='Todas las instituciones')
    sucursales = DjangoConnectionField(Sucursal, description='Todas las sucursales')

    def resolve_medicos(self, args, context, info):
        qs = models.Empleado.objects.medicos()
        if 'instituciones' in args:
            qs = qs.distinct()  # se aplica distinct para que no tire error cuando se usa aplica el filtro
        
        return qs
