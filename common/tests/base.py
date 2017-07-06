from rest_framework.test import APIClient
from tenant_schemas.test.cases import FastTenantTestCase
from tenant_schemas.test.client import TenantClient
from test_plus.test import TestCase


class BaseClient(TenantClient, APIClient):
    """Cliente base para las pruebas."""

    pass


class BaseTestCase(FastTenantTestCase, TestCase):
    """Clase base para pruebas unitarias."""

    def _pre_setup(self):
        super()._pre_setup()
        self.client = BaseClient(self.tenant)
    
    def login(self, usuario):
        self.client.login(username=usuario.username, password='adminadmin')