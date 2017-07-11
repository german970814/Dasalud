from unittest import mock
from django.test import tag
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

        self.get(self.URL, 34)
        self.response_404()

    def test_get_form(self):
        """Prueba que se muestre el formulario."""

        paciente = fac.PacienteFactory()
        self.get_check_200(self.URL, paciente.id)
        self.assertResponseContains('sucursal', html=False)

    def test_muestra_acompanante_vacio(self):
        """Prueba que si el paciente no tiene ordenes no se muestre ningún acompañante."""

        paciente = fac.PacienteFactory()

        self.get(self.URL, paciente.id)
        self.assertEqual(paciente.ordenes.count(), 0)
        self.assertIsNone(self.last_response.data['acompanante_s'].instance)

    def test_muestra_ultimo_acompanante(self, acompanante_mock):
        """Prueba que si el paciente tiene ordenes ingresadas se muestra un acompañante."""

        paciente = fac.PacienteFactory()
        fac.OrdenFactory(paciente=paciente)

        self.get(self.URL, paciente.id)
        self.assertTrue(paciente.ordenes.count() > 0, msg="El paciente debe tener ordenes.")
        self.assertIsNotNone(self.last_response.data['acompanante_s'].instance)


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

        self.post(self.URL, 34, extra={'format': 'json'})
        self.response_404()

    def test_crear_orden_invalida(self):
        """Prueba que si se envian los datos invalidos para crear una orden, la vista devuelva un 400."""

        paciente = fac.PacienteFactory()

        self.post(self.URL, paciente.id, data={}, extra={'format': 'json'})
        self.response_400()

    def test_crear_orden_valida(self):
        """Prueba que se si se envian los datos validos para crear una orden, esta se cree."""

        data = self.get_data()
        paciente = fac.PacienteFactory()
        self.post(self.URL, paciente.id, data=data, extra={'format': 'json'})

        self.response_201()
        self.assertEqual(Orden.objects.count(), 1)
