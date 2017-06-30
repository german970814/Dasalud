import factory
from .. import models

class EmpleadoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Empleado
    
    nombres = factory.Faker('first_name', locale='es')
    apellidos = factory.Faker('last_name', locale='es')
    cedula = factory.sequence(lambda n: '123456%02d' % n)

    class Params:
        medico = factory.Trait(tipo=models.Empleado.MEDICO)