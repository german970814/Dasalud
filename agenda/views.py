from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from pacientes.serializers import ServicioOrdenSerializer
from .serializers import HorarioAtencionSerializer
from .models import HorarioAtencion


class CitasViews(APIView):
    """Permite listar las citas agendadas por el cliente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'agenda/citas.html'

    def get(self, request):
        from pacientes.models import ServicioOrden
        citas = ServicioOrden.objects.select_related('servicio', 'orden', 'orden__paciente', 'orden__plan', 'orden__plan__empresa').all()
        serializer = ServicioOrdenSerializer(citas, many=True, expand=['orden', 'orden.paciente'], context={'request': None})
        citas_json = JSONRenderer().render(serializer.data)
        return Response({'citas': citas_json})


class HorarioAtencionMedicosView(generics.ListCreateAPIView):
    """Permite a un administrador agendar el horario de atención de los medicos."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'agenda/horario-atencion.html'
    serializer_class = HorarioAtencionSerializer
    queryset = HorarioAtencion.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('medico', 'sucursal')

    def get(self, request, *args, **kwargs):
        print(request.META.get('HTTP_ACCEPT'))
        if request.META.get('HTTP_ACCEPT', '').lower() == 'application/json':
            return super().get(request, *args, **kwargs)
        else:
            data = self.html_response()
            return Response(data)
        

    def html_response(self):
        from organizacional.serializers import SucursalSerializer, EmpleadoSerializer
        from organizacional.models import Sucursal, Empleado

        _sucursales = Sucursal.objects.all()
        _medicos = Empleado.objects.medicos()

        sucursales_s = SucursalSerializer(_sucursales, many=True)
        medicos_s = EmpleadoSerializer(_medicos, many=True)

        sucursales = JSONRenderer().render(sucursales_s.data)
        medicos = JSONRenderer().render(medicos_s.data)
        return {'sucursales': sucursales, 'medicos': medicos}