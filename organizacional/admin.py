from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.Institucion)
class InstitucionAdmin(VersionAdmin):
    pass


@admin.register(models.Empleado)
class EmpleadoAdmin(VersionAdmin):
    list_display = ['nombres', 'apellidos', 'agenda', 'sucursal']


@admin.register(models.Sucursal)
class SucursalAdmin(VersionAdmin):
    pass

