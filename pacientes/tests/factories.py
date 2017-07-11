import faker
import factory
import datetime
from .. import models


class PacienteFactory(factory.DjangoModelFactory):

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


class OrdenFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Orden
    
    paciente = factory.SubFactory(PacienteFactory)
    afiliacion = models.Orden.PARTICULAR
    tipo_usuario = models.Orden.PARTICULAR
    forma_pago = models.Orden.EFECTIVO
    plan = factory.SubFactory('servicios.tests.factories.PlanFactory')
    institucion = factory.SubFactory('organizacional.tests.factories.InstitucionFactory')
    sucursal = factory.SubFactory('organizacional.tests.factories.SucursalFactory')
    servicios = factory.RelatedFactory('pacientes.tests.factories.ServicioOrdenFactory', 'orden')
    acompanante = factory.RelatedFactory('pacientes.tests.factories.AcompananteFactory', 'orden')

class ServicioOrdenFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ServicioOrden
    
    orden = factory.SubFactory(OrdenFactory)
    servicio = factory.SubFactory('servicios.tests.factories.ServicioFactory')
    valor = 10000
    medico = factory.SubFactory('organizacional.tests.factories.EmpleadoFactory', medico=True)


class AcompananteFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Acompanante
    
    orden = factory.SubFactory(OrdenFactory, acompanante=None)
    asistio = True

    @factory.lazy_attribute
    def nombre(self):
        if self.asistio:
            return faker.Faker(locale='es').name()
        
        return ''
    
    @factory.lazy_attribute
    def direccion(self):
        if self.asistio:
            return faker.Faker(locale='es').address()
        
        return ''
    
    @factory.lazy_attribute
    def telefono(self):
        if self.asistio:
            return 3049459
        
        return None
    
