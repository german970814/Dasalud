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

    sesion = models.OneToOneField('pacientes.Sesion', verbose_name=_lazy('sesion'))
    contenido = fields.JSONField()
    terminada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'historia'
        verbose_name_plural = 'historias'
    
    def __str__(self):
        return '{0} - {1}'.format(self.pk, self.sesion)


def archivo_adjunto_path(instance, filename):
    """Path para el archivo adjunto."""

    return 'historia_{0}/adjuntos/{1}'.format(instance.historia_id, filename)


class Adjunto(models.Model):
    """Modelo que guarda los archivos adjuntos de una historia clinica."""

    archivo = models.FileField(upload_to=archivo_adjunto_path, verbose_name=_lazy('archivo'))
    historia = models.ForeignKey(Historia, related_name='adjuntos', verbose_name=_lazy('historia'))

    class Meta:
        verbose_name = 'adjunto'
        verbose_name_plural = 'adjuntos'
    

    def __str__(self):
        return '{0} - {1}'.format(self.historia, self.pk)

    # def delete(self, *args, **kwargs):
