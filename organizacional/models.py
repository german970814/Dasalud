from django.db import models
from django.utils.translation import ugettext_lazy as _lazy
from . import managers

class Sucursal(models.Model):
    """Modelo para guardar las sucursales de los clientes."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    direccion = models.CharField(_lazy('dirección'), max_length=100, blank=True)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)

    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'
    
    def __str__(self):
        return self.nombre


class Institucion(models.Model):
    """Modelo para guardar las instituciones que facturan."""


    NIT = 'NI'
    CEDULA_CIUDADANIA = 'CC'
    CEDULA_EXTRANJERIA = 'CE'
    TIPO_DOCUMENTOS = (
        (NIT, _lazy('NIT')),
        (CEDULA_CIUDADANIA, _lazy('Cédula de ciudadanía')),
        (CEDULA_EXTRANJERIA, _lazy('Cédula de extranjería'))
    )

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    razon_social = models.CharField(_lazy('razón social'), max_length=100)
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    identificacion = models.CharField(_lazy('identificación'), max_length=50, unique=True)
    codigo = models.CharField(_lazy('código'), max_length=50, blank=True)
    direccion = models.CharField(_lazy('dirección'), max_length=100)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)
    ciudad = models.ForeignKey('globales.Poblado', related_name='instituciones', verbose_name=_lazy('ciudad'))
    
    class Meta:
        verbose_name = 'institución'
        verbose_name_plural = 'instituciones'

    def __str__(self):
        return self.nombre

def empleado_firma_path(instance, filename):
    return 'empleado_{0}/firma_{1}'.format(instance.pk, filename)

class Empleado(models.Model):
    """Modelo para guardar los empleados de un cliente."""

    MEDICO = 'M'
    ADMINISTRATIVO = 'A'
    TIPOS = (
        (MEDICO, _lazy('medico')),
        (ADMINISTRATIVO, 'administrativo')
    )

    nombres = models.CharField(_lazy('nombres'), max_length=100)
    apellidos = models.CharField(_lazy('apellidos'), max_length=100)
    cedula = models.PositiveIntegerField(_lazy('cédula'))
    activo = models.BooleanField(_lazy('activo'), default=True)
    registro_medico = models.CharField(_lazy('registro medico'), max_length=100, blank=True)
    firma = models.ImageField(upload_to=empleado_firma_path ,verbose_name=_lazy('firma'), blank=True)
    tipo = models.CharField(_lazy('tipo'), max_length=2, choices=TIPOS, default=ADMINISTRATIVO)
    instituciones = models.ManyToManyField(Institucion, related_name='empleados', verbose_name=_lazy('instituciones'))
    duracion_cita = models.DurationField(
        _lazy('duración de las citas'), null=True, blank=True, help_text=_lazy('Ingresar duración de la forma HH:MM:SS')
    )

    # Managers
    objects = managers.EmpleadoManager()

    class Meta:
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)
