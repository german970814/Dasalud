import factory
from .. import models


class TipoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Tipo
        django_get_or_create = ('nombre', )
    
    nombre = 'CONSULTAS'


class ServicioFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Servicio
        django_get_or_create = ('nombre', )
    
    nombre = 'CONSULTA PRIMERA VEZ'
    codigo = factory.sequence(lambda n: '123456%02d' % n)
    abreviatura = 'CPV'
    tipo = factory.SubFactory(TipoFactory)
    formato = factory.SubFactory('historias.tests.factories.FormatoFactory')


class TarifaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Tarifa
        django_get_or_create = ('nombre', )
    
    nombre = 'PARTICULAR'
    servicios = factory.RelatedFactory('servicios.tests.factories.TarifaServicioFactory', 'tarifa')


class TarifaServicioFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.TarifaServicio
    
    tarifa = factory.SubFactory(TarifaFactory)
    servicio = factory.SubFactory(ServicioFactory)
    valor = 10000


class EmpresaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Empresa
        django_get_or_create = ('nombre', )
    
    nombre = 'PARTICULAR'
    razon_social = 'PARTICULAR'
    nit = factory.sequence(lambda n: '123456%02d' % n)


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Plan
        django_get_or_create = ('nombre', )
    
    nombre = 'PARTICULAR'
    empresa = factory.SubFactory(EmpresaFactory)
    tarifa = factory.SubFactory(TarifaFactory)