from django.contrib import admin
from . import models

admin.site.register(models.Empresa)
admin.site.register(models.Plan)
admin.site.register(models.Tipo)
admin.site.register(models.Servicio)
admin.site.register(models.Tarifa)
admin.site.register(models.TarifaServicio)
