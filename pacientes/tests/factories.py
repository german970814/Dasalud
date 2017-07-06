import factory
import datetime
from .. import models


class PacienteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Paciente
    
    nombres = factory.Faker('first_name', locale='es')
    apellidos = factory.Faker('last_name', locale='es')
    genero = models.Paciente.FEMENINO
    fecha_nacimiento = factory.Faker('date_time_this_century', before_now=True)
    fecha_ingreso = factory.LazyFunction(datetime.datetime.now)
    tipo_documento = models.Paciente.CEDULA_CIUDADANIA
    numero_documento = factory.sequence(lambda n: '112343%02d' % n)
    estado_civil = models.Paciente.SOLTERO
    zona = models.Paciente.URBANO
    direccion = factory.Faker('address', locale='es')
    email = factory.Faker('email')
    lugar_nacimiento = factory.SubFactory('globales.tests.factories.PobladoFactory')
    lugar_residencia = factory.SubFactory('globales.tests.factories.PobladoFactory')

    # Datos responsable
    nombre_responsable = factory.Faker('name', locale='es')
    direccion_responsable = factory.Faker('address', locale='es')
