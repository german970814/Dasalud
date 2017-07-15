import datetime
from django.test import tag
from freezegun import freeze_time
from common.tests.base import BaseTestCase
from . import factories as fac


class PacienteModelTest(BaseTestCase):
    """Pruebas unitarias para el modelo Paciente."""

    def setUp(self):
        self.paciente = fac.PacienteFactory()

    def test_ultimo_acompanante_returns_None(self):
        """Prueba que si un paciente no tiene ninguna orden asociada el acompañante sea None."""

        self.assertIsNone(self.paciente.ultimo_acompanante)

    def test_ultimo_acompanante(self):
        """Prueba que se devuelva el acompañante del paciente de la ultima orden registrada."""

        orden_nueva = fac.OrdenFactory(paciente=self.paciente)
        hace_20_dias = datetime.date.today() - datetime.timedelta(days=20)
        with freeze_time(hace_20_dias):
            fac.OrdenFactory(paciente=self.paciente)

        self.assertEqual(self.paciente.ultimo_acompanante, orden_nueva.acompanante)
