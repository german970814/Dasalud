import graphene
from graphene_django import DjangoObjectType
from . import models


class ServicioType(DjangoObjectType):

    class Meta:
        model = models.Servicio
        interfaces = (graphene.Node,)


class Query(graphene.AbstractType):
    pass
