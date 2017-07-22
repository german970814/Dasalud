from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

class Tipo(models.Model):
    """Modelo para guardar los tipos de servicio que presta un clinete."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)

    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'tipos'
    
    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    """Modelo para guardar la información de los servicios que ofrece un cliente."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    codigo = models.CharField(_lazy('código'), max_length=100, blank=True)
    abreviatura = models.CharField(_lazy('abreviatura'), max_length=100)
    cups = models.CharField(_lazy('cups'), max_length=100, blank=True)
    costo = models.PositiveIntegerField(_lazy('costo'), blank=True, null=True)
    tipo = models.ForeignKey(Tipo, related_name='servicios', verbose_name=_lazy('tipo'))
    formato = models.ForeignKey(
        'historias.Formato', related_name='servicios', verbose_name=_lazy('formato'), blank=True, null=True
    )

    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
    
    def __str__(self):
        return self.nombre


class Tarifa(models.Model):
    """Modelo para guardar las diferentes tarifas que maneja un cliente."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    servicios = models.ManyToManyField(
        Servicio, through='TarifaServicio', related_name='tarifas', verbose_name=_lazy('servicios')
    )

    class Meta:
        verbose_name = 'tarifa'
        verbose_name_plural = 'tarifas'
    
    def __str__(self):
        return self.nombre


class TarifaServicio(models.Model):
    """Modelo para guardar la información de la tarifa por servicio."""

    tarifa = models.ForeignKey(Tarifa, related_name='tarifas_servicio')
    servicio = models.ForeignKey(Servicio, related_name='tarifas_servicio')
    valor = models.PositiveIntegerField(_lazy('valor'))

    class Meta:
        verbose_name = 'tarifa por servicio'
        verbose_name_plural = 'tarifas por servicio'

    def __str__(self):
        return '{}-{}'.format(self.servicio.nombre, self.tarifa.nombre)


class Empresa(models.Model):
    """Modelo para guardar la información de las empresas a las cuales un cliente le presta sus servicios."""

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    razon_social = models.CharField(_lazy('razón social'), max_length=200)
    nit = models.CharField(_lazy('nit'), max_length=50)
    direccion = models.CharField(_lazy('dirección'), max_length=100, blank=True)
    telefono = models.PositiveIntegerField(_lazy('telefono'), blank=True, null=True)
    codigo = models.CharField(_lazy('código'), max_length=100, blank=True)
    ciudad = models.ForeignKey(
        'globales.Poblado', related_name='empresas', verbose_name=_lazy('ciudad'), blank=True, null=True
    )
    instituciones = models.ManyToManyField(
        'organizacional.Institucion', related_name='empresas', verbose_name=_lazy('instituciones')
    )

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
    
    def __str__(self):
        return self.nombre


class Plan(models.Model):
    """Modelo para guardar información de los planes que manejan las empresas."""

    nombre = models.CharField(_lazy('plan'), max_length=200)
    empresa = models.ForeignKey(Empresa, related_name='planes', verbose_name=_lazy('empresa'))
    tarifa = models.ForeignKey(Tarifa, related_name='planes', verbose_name=_lazy('tarifa'))

    class Meta:
        verbose_name = 'plan'
        verbose_name_plural = 'planes'
    
    def __str__(self):
        return '{} - {}'.format(self.empresa.nombre, self.nombre)
