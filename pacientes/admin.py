from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


class AcompananteInline(admin.StackedInline):
    model = models.Acompanante


class ServicioRealizarInline(admin.TabularInline):
    model = models.ServicioRealizar


@admin.register(models.Orden)
class OrdenAdmin(VersionAdmin):
    inlines = [AcompananteInline, ServicioRealizarInline]


@admin.register(models.Paciente)
class PacienteAdmin(VersionAdmin):
    pass

