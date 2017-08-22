import graphene
from graphene_django import DjangoConnectionField, DjangoObjectType
from . import models

class Empleado(DjangoObjectType):

    nombre_completo = graphene.String(source='__str__')

    class Meta:
        model = models.Empleado


class Query(graphene.AbstractType):
    pass

