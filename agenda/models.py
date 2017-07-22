from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


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