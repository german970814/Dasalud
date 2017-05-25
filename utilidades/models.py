from django.utils.translation import ugettext_lazy as _lazy
from django.db import models


class Profesion(models.Model):
    """Modelo para guardar las profesiones. Este modelo se maneja de manera global para todos los clientes."""

    nombre = models.CharField(_lazy('nombre'), max_length=250)
    codigo = models.CharField(_lazy('código'), max_length=3)

    class Meta:
        verbose_name = 'profesión'
        verbose_name_plural = 'profesiones'
    
    def __str__(self):
        return self.nombre
