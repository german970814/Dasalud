from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from pacientes.tests.factories import ServicioOrdenFactory
from .factories import AdjuntoFactory
from django.test import tag

@tag('actual')
class AdjuntosHistoriaViewTest(BaseTestCase):
    """Pruebas unitarias para la vista de adjuntos de una historia."""

    URL = 'historias:adjuntos'

    def setUp(self):
        self.login(UsuarioFactory())
    
    def test_get_servicio_no_existe_returns_404(self):
        """Prueba que si el servicio no existe devuelva un 404."""

        self.get(self.URL, 454)
        self.response_404()
    
    def test_get_adjuntos_servicio_indicado(self):
        """Prueba que solo devuelva los archivos adjuntos de la historia del servicio indicado."""

        otro_adjunto = AdjuntoFactory()
        servicio = ServicioOrdenFactory()
        AdjuntoFactory(historia__servicio_orden=servicio)

        self.get(self.URL, servicio.id, extra={'format': 'json'})
        self.response_200()
        self.assertEqual(len(self.last_response.data), 1)
    
    def test_post_servicio_no_existe_returns_404(self):
        """prueba que si el servicio no existe devuelva un 404."""

        self.post(self.URL, 343)
        self.response_404()
    
    def test_crear_adjunto_invalido(self):
        """Prueba que si se envian datos invalidos, la vista devuelva un 400."""

        servicio = ServicioOrdenFactory()
        self.post(self.URL, servicio.id, data={}, extra={'format': 'json'})
        self.response_400()
    
    def test_crear_adjunto(self):
        """Prueba que guarde el archivo adjunto."""

        data = {}
        servicio = ServicioOrdenFactory()
        self.post(self.URL, servicio.id, data=data, extra={'format': 'json'})
        # self.response_201() TODO probar que se suba el archivo