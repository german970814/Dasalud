from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.HorarioAtencion)
class HorarioAtencion(VersionAdmin):
    pass
