from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from pacientes.models import Paciente
from pacientes.serializers import ServicioOrdenSerializer
from .serializers import HorarioAtencionSerializer, CitaSerializer, PersonaSerializer
from .filters import CitaFilter
from .models import HorarioAtencion, Cita, Persona


class AgendaView(APIView):
    """Permite listar la agenda de los medicos."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'agenda/agenda.html'

    def get(self, request):
        from pacientes.models import ServicioOrden
        citas = ServicioOrden.objects.select_related('servicio', 'orden', 'orden__paciente', 'orden__plan', 'orden__plan__empresa').all()
        serializer = ServicioOrdenSerializer(citas, many=True, expand=['orden', 'orden.paciente'], context={'request': None})
        citas_json = JSONRenderer().render(serializer.data)
        return Response({'citas': citas_json})


class HorarioAtencionMedicosView(generics.ListCreateAPIView):
    """Permite agendar el horario de atención de los medicos."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'agenda/horario-atencion.html'
    serializer_class = HorarioAtencionSerializer
    queryset = HorarioAtencion.objects.all()
    filter_fields = ('medico', 'sucursal')

    def get(self, request, *args, **kwargs):
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


class CitasView(generics.ListCreateAPIView):
    """Permite agendar citas a un medico."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'agenda/citas.html'
    serializer_class = CitaSerializer
    queryset = Cita.objects.all()
    filter_class = CitaFilter

    def get(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)
        if request.META.get('HTTP_ACCEPT', '').lower() == 'application/json':
            return super().get(request, *args, **kwargs)
        else:
            data = self.html_response()
            return Response(data)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        expand = ['paciente']
        return super().get_serializer(expand=expand, *args, **kwargs)

    def html_response(self):
        from organizacional.serializers import SucursalSerializer, EmpleadoSerializer
        from organizacional.models import Sucursal, Empleado

        _sucursales = Sucursal.objects.all()
        _medicos = Empleado.objects.medicos()

        sucursales_s = SucursalSerializer(_sucursales, many=True)
        medicos_s = EmpleadoSerializer(_medicos, many=True)

        sucursales = JSONRenderer().render(sucursales_s.data)
        medicos = JSONRenderer().render(medicos_s.data)

        form = CitaSerializer(fields=['paciente', 'servicio', 'estado'], expand=['paciente'])
        return {'sucursales': sucursales, 'medicos': medicos, 'form': form}


class CitaDetailView(generics.RetrieveUpdateAPIView):
    """Permite editar una cita."""

    serializer_class = CitaSerializer
    queryset = Cita.objects.all()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(expand=['paciente'], *args, **kwargs)


class BuscarPersonaView(APIView):
    """Permite buscar una persona por numero de documento.
    
    La persona se busca primero como un paciente y luego como una persona."""

    def get(self, request):
        numero = request.GET.get('q', None)

        if not numero:
            raise Http404

        try:
            persona = get_object_or_404(Paciente, numero_documento=numero)
        except:
            persona = get_object_or_404(Persona, numero_documento=numero)
    
        serializer = PersonaSerializer(persona)
        return Response(serializer.data)
