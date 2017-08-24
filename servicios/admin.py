from django.contrib import admin
from . import models

class PlanInline(admin.TabularInline):
    model = models.Plan


class EmpresaAdmin(admin.ModelAdmin):
    inlines = [PlanInline]


class TarifaInline(admin.TabularInline):
    model = models.Tarifa


class PlanAdmin(admin.ModelAdmin):
    inlines = [TarifaInline]

admin.site.register(models.Empresa, EmpresaAdmin)
admin.site.register(models.Tipo)
admin.site.register(models.Servicio)
admin.site.register(models.Plan, PlanAdmin)
