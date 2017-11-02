import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from common.schema import BaseNode

from . import models
from . import filters


class Historia(DjangoObjectType):

    class Meta:
        model = models.Historia
        interfaces = (BaseNode,)


class Query(graphene.AbstractType):
    historia = BaseNode.Field(Historia)
    historias = DjangoFilterConnectionField(Historia, filterset_class=filters.HistoriaFilter, description='Todas las historias')
