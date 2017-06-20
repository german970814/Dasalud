from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _lazy
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters

from .models import Paciente, Orden
from .serializers import PacienteSerializer, OrdenSerializer, AcompananteSerializer, ServicioOrdenSerializer
from .serializers import CrearOrdenSerializer


class PacientesList(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombres', 'apellidos', 'numero_documento')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = None
        return context

class OrdenesList(generics.ListCreateAPIView):
    queryset = Orden.objects.all()
    serializer_class = CrearOrdenSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = None
        return context


class ListarPacientesView(generics.ListCreateAPIView):
    """Permite listar y crear pacientes."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/lista_pacientes.html'
    serializer_class = PacienteSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombres', 'apellidos', 'numero_documento')

    def get(self, request):
        queryset = self.filter_queryset(Paciente.objects.all())
        serializer = PacienteSerializer(queryset, many=True, context={'request': None})
        pacientes = JSONRenderer().render(serializer.data)
        return Response({'pacientes': pacientes, 'total_pacientes': len(serializer.data)})


class PacienteDetalleView(generics.UpdateAPIView):
    """Permite editar un paciente."""

    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()

class CrearPacienteView(APIView):
    """Muestra el formulario de creación de un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/paciente_form.html'
    VERBO = _lazy('Crear')
    URL = reverse_lazy('pacientes:listar')
    MSJ = _lazy('Paciente creado correctamente')
    METHOD = 'POST'

    def get(self, request):
        form = PacienteSerializer(context={'request': None})
        return Response({'form': form, 'VERBO': self.VERBO, 'URL': self.URL, 'MSJ': self.MSJ, 'METHOD': self.METHOD})

class EditarPacienteView(APIView):
    """Muestra el formulario de creación de un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/paciente_form.html'
    VERBO = _lazy('Editar')
    MSJ = _lazy('Paciente editado correctamente')
    METHOD = 'PUT'

    def get(self, request, pk):
        self.URL = reverse_lazy('pacientes:detalle', args=[pk])
        paciente = get_object_or_404(Paciente, pk=pk)
        form = PacienteSerializer(paciente, context={'request': None})
        return Response({'form': form, 'VERBO': self.VERBO, 'URL': self.URL, 'MSJ': self.MSJ, 'METHOD': self.METHOD})


class BucarPacientesView(generics.GenericAPIView):
    """Permite buscar un paciente según sus nombres, apellidos y número de documento."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/resultado_busqueda.html'
    serializer_class = PacienteSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombres', 'apellidos', 'numero_documento')

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Paciente.objects.all())
        serializer = PacienteSerializer(queryset, many=True, context={'request': None})
        pacientes = JSONRenderer().render(serializer.data)
        return Response({'pacientes': pacientes})

class CrearOrdenView(APIView):
    """Muestra el formulario de creación de una orden para un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/orden_form.html'
    VERBO = _lazy('Crear')

    def get(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, context={'request': None})
        paciente_json = JSONRenderer().render(serializer.data)
        orden_s = OrdenSerializer()
        acompanante_s = AcompananteSerializer()
        servicios_s = ServicioOrdenSerializer()

        return Response({
            'paciente': paciente_json, 'orden_s': orden_s, 'servicios_s': servicios_s,
            'acompanante_s': acompanante_s, 'VERBO': self.VERBO, 'paciente_id': pk
        })


class OrdenesPacienteView(generics.CreateAPIView):
    """Permite crear una orden a un paciente."""

    serializer_class = CrearOrdenSerializer

    def post(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, pk=kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(paciente=self.paciente)



