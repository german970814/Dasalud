import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from django.core.urlresolvers import reverse
from common.schema import BaseNode

from . import models
from . import filters


class Historia(DjangoObjectType):

    sesion_url = graphene.String()

    class Meta:
        model = models.Historia
        interfaces = (BaseNode,)

    def resolve_sesion_url(self, args, context, info):
        return reverse('pacientes:historias', args=(self.sesion.id, ))
        


class Query(graphene.AbstractType):
    historia = BaseNode.Field(Historia)
    historias = DjangoFilterConnectionField(Historia, filterset_class=filters.HistoriaFilter, description='Todas las historias')
