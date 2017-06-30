from unittest import mock
from django.urls import reverse
from rest_framework import status
from common.tests.base import BaseTestCase
from . import factories as fac


class MedicosViewTest(BaseTestCase):
    """Pruebas unitarias para la vista que permite listar medicos."""

    URL = 'organizacional:medicos'

    def test_get_medicos(self):
        """Prueba que se listen los medicos."""

        # TODO probar que se llame al queryset medicos
        response = self.client.get(reverse(self.URL))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



