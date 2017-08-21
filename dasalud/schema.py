import graphene
import agenda.schema
import servicios.schema
from graphene_django.debug import DjangoDebug


class Query(
    servicios.schema.Query,
    agenda.schema.Query,
    graphene.ObjectType
):
    """Base entry point to the schema. Inherits from all other schemas."""

    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)