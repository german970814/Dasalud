from django.db import models

class EmpleadoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo empleado."""

    def medicos(self):
        """
        :returns:
            Un queryset con los empleados que son de tipo medico.
        """

        return self.filter(tipo=self.model.MEDICO)

class EmpleadoManager(models.Manager.from_queryset(EmpleadoQuerySet)):
    """Manager personalizado para el modelo Empleado."""

    pass