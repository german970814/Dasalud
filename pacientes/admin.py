from django.contrib import admin
from . import models

class AcompananteInline(admin.StackedInline):
    model = models.Acompanante

class ServiciosOrdenInline(admin.TabularInline):
    model = models.ServicioOrden


class OrdenAdmin(admin.ModelAdmin):
    inlines = [AcompananteInline, ServiciosOrdenInline]


admin.site.register(models.Paciente)
admin.site.register(models.Orden, OrdenAdmin)

