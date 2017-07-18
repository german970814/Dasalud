import factory
from .. import models


class FormatoFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Formato
        django_get_or_create = ('nombre',)

    nombre = 'HISTORIA CLINICA'
    contenido = [{'nombre': 'CONDUCTA', 'fields': [
                    [{'tipo': 'text', 'nombre': 'Diagnostico', 'required': True}],
                    [{'tipo': 'textarea', 'nombre': 'Desayuno'}]
                ]}]


class HistoriaFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Historia

    servicio_orden = factory.SubFactory('pacientes.tests.factories.ServicioOrdenFactory')
    contenido = [{'nombre': 'CONDUCTA', 'fields': [
                    [{'tipo': 'text', 'nombre': 'Diagnostico', 'required': True}],
                    [{'tipo': 'textarea', 'nombre': 'Desayuno'}]
                ]}]


class AdjuntoFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Adjunto
    
    historia = factory.SubFactory(HistoriaFactory)
    archivo = factory.django.FileField()
