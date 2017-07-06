import factory
from .. import models


class ProfesionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Profesion
    
    codigo = factory.Faker('pyint')
    nombre = factory.Faker('job', locale='es')


class DepartamentoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Departamento
        django_get_or_create = ('nombre', )
    
    nombre = 'Atlantico'
    codigo = factory.Faker('pyint')


class MunicipioFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Municipio
        django_get_or_create = ('nombre', )
    
    nombre = 'Barranquilla'
    codigo = factory.Faker('pyint')
    departamento = factory.SubFactory(DepartamentoFactory)


class PobladoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Poblado
        django_get_or_create = ('nombre', )
    
    nombre = 'Barranquilla'
    codigo = factory.Faker('pyint')
    municipio = factory.SubFactory(MunicipioFactory)


class CieFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Cie
    
    codigo = factory.Faker('pyint')
    nombre = 'ABDOMEN AGUDO'