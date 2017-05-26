"""Estos modelos se manejan de manera global para todos los clientes."""

from django.utils.translation import ugettext_lazy as _lazy
from django.db import models


class Profesion(models.Model):
    """Modelo para guardar las profesiones."""

    nombre = models.CharField(_lazy('nombre'), max_length=250)
    codigo = models.IntegerField(_lazy('código'))

    class Meta:
        verbose_name = 'profesión'
        verbose_name_plural = 'profesiones'
    
    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    """Modelo para guardar los departamentos."""

    codigo = models.IntegerField(_lazy('código'))
    nombre = models.CharField(_lazy('nombre'), max_length=250)

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
    
    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    """Modelo para guardar los municipios."""

    codigo = models.IntegerField(_lazy('código'))
    nombre = models.CharField(_lazy('nombre'), max_length=250)

    class Meta:
        verbose_name = 'municipio'
        verbose_name_plural = 'municipios'
    
    def __str__(self):
        return self.nombre

class Poblado(models.Model):
    """Modelo para guardar los poblados."""

    codigo = models.IntegerField(_lazy('código'))
    nombre = models.CharField(_lazy('nombre'), max_length=250)

    class Meta:
        verbose_name = 'poblado'
        verbose_name_plural = 'poblados'
    
    def __str__(self):
        return self.nombre
