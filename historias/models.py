from django.db import models
from django.utils.translation import ugettext_lazy as _lazy
from django.contrib.postgres import fields


class Formato(models.Model):
    """Modelo que guarda el formato de las historias clinicas de los pacientes."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    contenido = fields.JSONField()

    class Meta:
        verbose_name = 'formato'
        verbose_name_plural = 'formatos'
    
    def __str__(self):
        return self.nombre


class Historia(models.Model):
    """Modelo que guarda las historias clinicas de un paciente."""

    servicio_orden = models.OneToOneField('pacientes.ServicioOrden', verbose_name=_lazy('servicio'))
    historia = fields.JSONField()
    terminada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'historia'
        verbose_name_plural = 'historias'
    
    def __str__(self):
        return ''.format(self.servicio_orden)
