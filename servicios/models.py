from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

class Servicio(models.Model):
    """Modelo para guardar la información de los servicios que ofrece un cliente."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)

    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
    
    def __str__(self):
        return self.nombre

class Empresa(models.Model):
    """Modelo para guardar la información de las empresas a las cuales un cliente le presta sus servicios."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
    
    def __str__(self):
        return self.nombre

class Plan(models.Model):
    """Modelo para guardar información de los planes que manejan las empresas"""

    nombre = models.CharField(_lazy('plan'), max_length=200)
    empresa = models.ForeignKey(Empresa, related_name='planes', verbose_name=_lazy('empresa'))
    servicios = models.ManyToManyField(Servicio, related_name='planes', verbose_name=_lazy('servicios'))

    class Meta:
        verbose_name = 'plan'
        verbose_name_plural = 'planes'
    
    def __str__(self):
        return self.nombre
