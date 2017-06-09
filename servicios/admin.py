from django.contrib import admin
from . import models

class PlanInline(admin.TabularInline):
    model = models.Plan


class EmpresaAdmin(admin.ModelAdmin):
    inlines = [PlanInline]


class TarifaServicioInline(admin.TabularInline):
    model = models.TarifaServicio

class TarifaAdmin(admin.ModelAdmin):
    inlines = [TarifaServicioInline]


admin.site.register(models.Empresa, EmpresaAdmin)
admin.site.register(models.Tipo)
admin.site.register(models.Servicio)
admin.site.register(models.Tarifa, TarifaAdmin)
