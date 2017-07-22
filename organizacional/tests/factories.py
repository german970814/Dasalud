import factory
import datetime
from .. import models

class EmpleadoFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Empleado
    
    nombres = factory.Faker('first_name', locale='es')
    apellidos = factory.Faker('last_name', locale='es')
    cedula = factory.sequence(lambda n: '123456%02d' % n)

    class Params:
        medico = factory.Trait(
            tipo=models.Empleado.MEDICO,
            registro_medico=factory.sequence(lambda n: 'RM123456%02d' % n),
            duracion_cita=datetime.timedelta(minutes=30)
        )


class MedicoFactory(EmpleadoFactory):
    medico = True


class SucursalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Sucursal
        django_get_or_create = ('nombre', )
    
    nombre = 'NORTE'


class InstitucionFactory(factory.DjangoModelFactory):
    
    class Meta:
        model = models.Institucion
        django_get_or_create = ('nombre', )
    
    nombre = 'DASALUD'
    razon_social = 'DASALUD'
    tipo_documento = models.Institucion.NIT
    identificacion = factory.sequence(lambda n: '123456%02d' % n)
    direccion = factory.Faker('address', locale='es')
    ciudad = factory.SubFactory('globales.tests.factories.PobladoFactory')