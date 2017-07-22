import datetime
from django.test import tag
from django.utils import timezone
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from organizacional.tests.factories import MedicoFactory, SucursalFactory
from ..models import HorarioAtencion


@tag('actual')
class HorarioAtencionMedicosViewTest(BaseTestCase):
    """Pruebas unitarias para la vista horario de atención de los medicos."""

    URL = 'agenda:horario-atencion'

    def setUp(self):
        self.login(UsuarioFactory())
    
    def test_get_horario_atencion(self):
        """Prueba que se muestre la vista para ingresar el horario de atención de un medico."""

        self.get_check_200(self.URL)
        self.assertResponseContains('horario de atención', html=False)
    
    def test_post_horario_atencion_invalido(self):
        """Prueba que si se envia una POST con datos invalidos no se guarde nada."""

        self.post(self.URL, data={})
        self.response_400()
    
    def test_post_crea_horario_atencion(self):
        """Prueba que si se envia un POST con datos validos se cree un horario de atención."""

        medico = MedicoFactory()
        sucursal = SucursalFactory()
        start = timezone.now()
        end = start + medico.duracion_cita
        data = {'medico': medico.id, 'sucursal': sucursal.id, 'start': start, 'end': end}

        self.post(self.URL, data=data, extra={'format': 'json'})
        self.response_201()
        self.assertEqual(HorarioAtencion.objects.count(), 1)