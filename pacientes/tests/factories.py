import factory
from .. import models


class PacienteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Paciente
    
    nombres = factory.Faker('first_name', locale='es')
    apellidos = factory.Faker('last_name', locale='es')
    genero = 'F'