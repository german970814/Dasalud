from django.urls import reverse
from rest_framework import status
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from . import factories as fac

class CrearOrdenViewTest(BaseTestCase):
    """Pruebas unitarias para la vista que muestra el formulario de creación de una orden."""

    URL = 'pacientes:ordenes-nueva'

    def setUp(self):
        self.paciente = fac.PacienteFactory()
        self.login(UsuarioFactory())

    def test_get_form(self):
        """Prueba que se muestre el formulario."""

        response = self.client.get(reverse(self.URL, args=(self.paciente.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'sucursal')