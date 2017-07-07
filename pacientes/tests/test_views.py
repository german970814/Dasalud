from django.urls import reverse
from django.test import tag
from rest_framework import status
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from . import factories as fac
from ..models import Orden

class CrearOrdenViewTest(BaseTestCase):
    """Pruebas unitarias para la vista que muestra el formulario de creación de una orden."""

    URL = 'pacientes:ordenes-nueva'

    def setUp(self):
        self.login(UsuarioFactory())
    
    def test_get_paciente_no_existe_returns_404(self):
        """Prueba que si el paciente no existe la vista devuelva un 404."""

        response = self.client.get(reverse(self.URL, args=(34, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_form(self):
        """Prueba que se muestre el formulario."""

        paciente = fac.PacienteFactory()
        response = self.client.get(reverse(self.URL, args=(paciente.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'sucursal')

@tag('actual')
class OrdenesPacienteViewTest(BaseTestCase):
    """Pruebas unitarias para la vista para guardar las ordenes de un paciente."""

    URL = 'pacientes:ordenes'

    def setUp(self):
        self.login(UsuarioFactory())
    
    def get_data(self):
        from organizacional.tests.factories import InstitucionFactory, SucursalFactory, EmpleadoFactory
        from servicios.tests.factories import PlanFactory, TarifaFactory
        from servicios.models import TarifaServicio, Servicio
        from pacientes.models import ServicioOrden

        s = SucursalFactory()
        i = InstitucionFactory()
        p = PlanFactory()
        e = EmpleadoFactory(medico=True)
        se = Servicio.objects.first()

        data = {
            'sucursal': s.id, 'autorizacion': '23424', 'pendiente_autorizacion': False, 'institucion': i.id, 'plan': p.id,
            'afiliacion': Orden.PARTICULAR, 'tipo_usuario': Orden.PARTICULAR, 'forma_pago': Orden.TARJETA,
            'acompanante': {
                'asistio': True, 'nombre': 'Maria medina', 'direccion': 'Cra 34 N 34 - 54', 'telefono': '3433334'
            },
            'servicios': [
                {'medico': e.id, 'servicio': se.id, 'tipo_pago': ServicioOrden.COOPAGO, 'valor': 10000, 'descuento': 0},
                {'medico': e.id, 'servicio': se.id, 'tipo_pago': ServicioOrden.COOPAGO, 'valor': 10000, 'descuento': 0}
            ]            
        }

        return data

    
    def test_post_paciente_no_existe_returns_404(self):
        """Prueba que si el paciente no existe la vista devuelva un 404."""

        response = self.client.post(reverse(self.URL, args=(34, )), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_crear_orden_invalida(self):
        """Prueba que si se envian los datos invalidos para crear una orden, la vista devuelva un 400."""

        paciente = fac.PacienteFactory()
        response = self.client.post(reverse(self.URL, args=(paciente.id,)), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_orden_valida(self):
        """Prueba que se si se envian los datos validos para crear una orden, esta se cree."""

        data = self.get_data()
        paciente = fac.PacienteFactory()
        response = self.client.post(reverse(self.URL, args=(paciente.id,)), data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Orden.objects.count(), 1)
    
