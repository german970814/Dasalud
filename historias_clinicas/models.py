from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


class Paciente(models.Model):
    """Modelo para guardar la información de un paciente."""

    FEMENINO = 'F'
    MASCULINO = 'M'
    GENEROS = (
        (FEMENINO, 'Femenino'),
        (MASCULINO, 'Masculino'),
    )

    nombres = models.CharField(_lazy('nombres'), max_length=150)
    apellidos = models.CharField(_lazy('apellidos'), max_length=150)
    genero = models.CharField(_lazy('genero'), max_length=1, choices=GENEROS)
    fecha_nacimiento = models.DateField(_lazy('fecha de nacimiento'))
    tipo_sangre = models.CharField(_lazy('tipo de sangre'), max_length=1)
    fecha_ingreso = models.DateField(_lazy('fecha de ingreso'))


