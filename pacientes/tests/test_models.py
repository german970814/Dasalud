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


class ServicioOrdenModelTest(BaseTestCase):
    """Pruebas unitarias para el modelo ServicioOrden."""

    def setUp(self):
        self.servicio_orden = fac.ServicioOrdenFactory()

    def test_get_historia_returns_None(self):
        """Prueba que devuelva None si el servicio no tiene historia guardada."""

        from historias.models import Historia

        historia = self.servicio_orden.get_historia()
        self.assertIsNone(historia)
    
    def test_get_historia(self):
        """Prueba que devuelva la historia del servicio si ya la tiene guardada."""

        from historias.tests.factories import HistoriaFactory

        h = HistoriaFactory(servicio_orden=self.servicio_orden)
        historia = self.servicio_orden.get_historia()
        self.assertIsNotNone(historia)
        self.assertEqual(h, historia)
    
    def test_get_historia_returns_instance(self):
        """Prueba que devuelva una instancia de historia si el servicio no tiene historia guardada."""

        from historias.models import Historia

        historia = self.servicio_orden.get_historia(force_instance=True)
        self.assertIsInstance(historia, Historia)
        self.assertEqual(historia.contenido, self.servicio_orden.servicio.formato.contenido)


