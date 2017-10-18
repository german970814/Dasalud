import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from common.schema import BaseNode
from .filters import PlanFilter
from . import models


class Servicio(DjangoObjectType):

    pk = graphene.Int(source='pk')

    class Meta:
        model = models.Servicio
        interfaces = (BaseNode,)
        filter_fields = ['planes']


class Cliente(DjangoObjectType):

    class Meta:
        model = models.Cliente
        interfaces = (BaseNode,)


class Plan(DjangoObjectType):

    label = graphene.String(source='__str__')

    class Meta:
        model = models.Plan
        interfaces = (BaseNode,)


class Tarifa(DjangoObjectType):

    class Meta:
        model = models.Tarifa
        interfaces = (BaseNode,)
        filter_fields = ['servicio', 'plan']


class Query(graphene.AbstractType):
    servicios = DjangoFilterConnectionField(Servicio, description='Todos los servicios')
    planes = DjangoFilterConnectionField(Plan, filterset_class=PlanFilter, description='Todos los planes')
