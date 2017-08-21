from django.db import models
from django.utils.translation import ugettext_lazy as _lazy
from common.models import UpdateModelMixin


class HorarioAtencion(models.Model):
    """Modelo que guarda el horario de atención que un medico maneja en una sucursal."""

    title = models.CharField(_lazy('titulo'), max_length=100, default='')
    start = models.DateTimeField(_lazy('inicio'))
    end = models.DateTimeField(_lazy('final'))
    medico = models.ForeignKey('organizacional.Empleado', related_name='horario_atencion')
    sucursal = models.ForeignKey('organizacional.Sucursal', related_name='horario_atencion')

    class Meta:
        verbose_name = 'horario de atención'
        verbose_name_plural = 'horarios de atención'

    def __str__(self):
        return '{} - {} - {}'.format(self.sucursal, self.medico, self.start)


class Persona(UpdateModelMixin, models.Model):
    """Modelo para guardar información basica de la persona que esta agendando la cita."""

    MENOR_NN = 'MN'
    ADULTO_NN = 'AN'
    PASAPORTE = 'PA'
    REGISTRO_CIVIL = 'RC'
    NUMERO_UNICO_ID = 'NU'
    CEDULA_CIUDADANIA = 'CC'
    TARJETA_IDENTIDAD = 'TI'
    CEDULA_EXTRANJERIA = 'CE'
    TIPO_DOCUMENTOS = (
        (CEDULA_CIUDADANIA, _lazy('Cédula de ciudadanía')),
        (CEDULA_EXTRANJERIA, _lazy('Cédula de extranjería')),
        (PASAPORTE, _lazy('Pasaporte')),
        (REGISTRO_CIVIL, _lazy('Registro civil')),
        (TARJETA_IDENTIDAD, _lazy('Tarjeta de identidad')),
        (ADULTO_NN, _lazy('Adulto sin identificar')),
        (MENOR_NN, _lazy('Menor sin identificar')),
        (NUMERO_UNICO_ID, 'Número único de identificación')
    )

    nombres = models.CharField(_lazy('nombres'), max_length=150)
    apellidos = models.CharField(_lazy('apellidos'), max_length=150)
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    numero_documento = models.CharField(_lazy('número de documento'), max_length=20, unique=True)
    telefono = models.PositiveIntegerField(_lazy('telefono'), null=True, blank=True)
    celular = models.IntegerField(_lazy('celular'), null=True, blank=True)
    direccion = models.CharField(_lazy('dirección'), max_length=200, blank=True)

    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)


class Cita(UpdateModelMixin, models.Model):
    """Modelo para guardar las citas de un medico."""

    CUMPLIDA = 'CU'
    EXCUSADA = 'EX'
    CANCELADA = 'CA'
    CONFIRMADA = 'CO'
    NO_ASISTIO = 'NA'
    NO_CONFIRMADA = 'NC'
    ESTADOS = (
        (NO_CONFIRMADA, _lazy('No confirmada')),
        (CONFIRMADA, _lazy('Confirmada')),
        (CUMPLIDA, _lazy('Cumplida')),
        (CANCELADA, _lazy('Cancelada')),
        (EXCUSADA, _lazy('Excusada')),
        (NO_ASISTIO, _lazy('No asistio')),
    )

    paciente = models.ForeignKey(Persona, related_name='citas', verbose_name=_lazy('paciente'))
    servicio = models.ForeignKey('servicios.Servicio', related_name='citas', verbose_name=_lazy('servicio'))
    horario = models.ForeignKey(HorarioAtencion, related_name='citas', verbose_name=_lazy('horario'))
    estado = models.CharField(_lazy('estado'), max_length=2, choices=ESTADOS)
    sesion = models.OneToOneField('pacientes.Sesion', verbose_name=_lazy('sesión'), null=True, blank=True)

    class Meta:
        verbose_name = 'cita'
        verbose_name_plural = 'citas'
    
    def __str__(self):
        return '{}'.format(self.paciente)

    @property
    def start(self):
        return self.horario.start

    @property
    def end(self):
        return self.horario.end

    @property
    def cumplida(self):
        return self.estado == self.CUMPLIDA
