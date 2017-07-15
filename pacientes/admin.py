from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


class AcompananteInline(admin.StackedInline):
    model = models.Acompanante


class ServiciosOrdenInline(admin.TabularInline):
    model = models.ServicioOrden


@admin.register(models.Orden)
class OrdenAdmin(VersionAdmin):
    inlines = [AcompananteInline, ServiciosOrdenInline]


@admin.register(models.Paciente)
class PacienteAdmin(VersionAdmin):
    pass

