from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


class PersonaInline(admin.TabularInline):
    model = models.Persona


@admin.register(models.HorarioAtencion)
class HorarioAtencionAdmin(VersionAdmin):
    pass


@admin.register(models.Cita)
class CitaAdmin(VersionAdmin):
    pass


@admin.register(models.Persona)
class PersonaAdmin(VersionAdmin):
    pass
