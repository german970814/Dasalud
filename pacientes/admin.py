from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


class AcompananteInline(admin.StackedInline):
    model = models.Acompanante


class ServicioRealizarInline(admin.TabularInline):
    model = models.ServicioRealizar


class SesionInline(admin.TabularInline):
    model = models.Sesion


@admin.register(models.Orden)
class OrdenAdmin(VersionAdmin):
    inlines = [AcompananteInline, ServicioRealizarInline]


@admin.register(models.Paciente)
class PacienteAdmin(VersionAdmin):
    pass


@admin.register(models.ServicioRealizar)
class ServicioRealizarAdmin(VersionAdmin):
    inlines = [SesionInline]

