import graphene
import agenda.schema
import servicios.schema
import organizacional.schema
import pacientes.schema
from graphene_django.debug import DjangoDebug


class Query(
    organizacional.schema.Query,
    servicios.schema.Query,
    agenda.schema.Query,
    pacientes.schema.Query,
    graphene.ObjectType
):
    """Base entry point to the schema. Inherits from all other schemas."""

    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)