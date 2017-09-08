from django.contrib import admin
from reversion.admin import VersionAdmin
from .  import models


@admin.register(models.Historia)
class HistoriaAdmin(VersionAdmin):
    pass


@admin.register(models.Formato)
class FormatoAdmin(VersionAdmin):
    pass


@admin.register(models.Adjunto)
class AdjuntoAdmin(VersionAdmin):
    pass
