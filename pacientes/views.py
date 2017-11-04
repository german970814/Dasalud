from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters, status

from dasalud.schema import schema
from common.schema import BaseNode
from agenda.models import Cita
from historias.serializers import HistoriaSerializer
from .models import Paciente, Orden, Sesion
from .serializers import PacienteSerializer, OrdenSerializer, AcompananteSerializer
from . import serializers


class PacientesList(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_documento')
    filter_fields = ('numero_documento',)


class OrdenesList(generics.ListCreateAPIView):
    queryset = Orden.objects.all()
    serializer_class = serializers.OrdenSerializer

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(expand=['servicios_realizar.sesiones'], *args, **kwargs)


class ListarPacientesView(generics.ListCreateAPIView):
    """Permite buscar un paciente según sus nombres, apellidos o número de documento y crear pacientes."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/lista_pacientes.html'
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_documento')
    filter_fields = ('numero_documento',)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT', '').lower() == 'application/json':
            return super().get(request, *args, **kwargs)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = PacienteSerializer(queryset, many=True, context={'request': request})
            pacientes = JSONRenderer().render(serializer.data)
            return Response({'pacientes': pacientes})


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
        paciente = None
        cita = request.session.get('cita', None)
        if cita:
            paciente = Paciente(**request.session.pop('paciente-cita', {}))
        form = PacienteSerializer(paciente, context={'request': request})
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
        form = PacienteSerializer(paciente, context={'request': request})
        return Response({'form': form, 'VERBO': self.VERBO, 'URL': self.URL, 'MSJ': self.MSJ, 'METHOD': self.METHOD})


class CrearOrdenView(APIView):
    """Muestra el formulario de creación de una orden para un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/orden_form.html'
    VERBO = _lazy('Crear')

    def get(self, request, pk):        
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, context={'request': request})
        paciente_json = JSONRenderer().render(serializer.data)

        orden_s = serializers.OrdenSerializer(fields=['sucursal', 'institucion', 'plan', 'afiliacion', 'tipo_usuario'])
        acompanante_s = AcompananteSerializer(paciente.ultimo_acompanante)

        cita = None
        request.session.pop('paciente-cita', None)
        cita_id = request.session.get('cita', None)
        if cita_id:
            # TODO una vez se usa graphql para guardar la cita quitar to_global_id. id ej: "Q2l0YTox"
            cita = BaseNode.to_global_id('Cita', cita_id)

        return Response({
            'paciente': paciente_json, 'orden_s': orden_s, 'cita': cita,
            'acompanante_s': acompanante_s, 'VERBO': self.VERBO, 'paciente_id': pk
        })


class EditarOrdenView(generics.RetrieveUpdateAPIView):
    """Muestra el formulario de edicion de una orden."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/orden_form.html'
    serializer_class = serializers.OrdenSerializer
    VERBO = _lazy('Editar')

    def get(self, request, paciente, pk):
        cita = None
        self.paciente = get_object_or_404(Paciente, pk=paciente)
        orden = self.get_object()
        serializer = PacienteSerializer(self.paciente, context={'request': request})
        paciente_json = JSONRenderer().render(serializer.data)

        orden_s = serializers.OrdenSerializer(
            orden, fields=['institucion', 'plan', 'afiliacion', 'tipo_usuario']
        )

        return Response({
            'paciente': paciente_json, 'orden_s': orden_s, 'cita': cita, 'orden': BaseNode.to_global_id('Orden', pk),
            'VERBO': self.VERBO, 'paciente_id': self.paciente.id, 'edit': True, 'orden_pk': pk
        })
    
    def put(self, request, paciente, pk, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, pk=paciente)
        response = super().put(request, *args, **kwargs)
        return response

    def get_queryset(self):
        return self.paciente.ordenes.all()

    def get_serializer(self, *args, **kwargs):
        fields = [
            'id', 'institucion', 'plan', 'afiliacion', 'orden_link',
            'tipo_usuario', 'acompanante', 'servicios_realizar'
        ]
        expand = ['acompanante', 'servicios_realizar.sesiones']
        return super().get_serializer(fields=fields, expand=expand, *args, **kwargs)


class OrdenesPacienteView(generics.CreateAPIView):
    """Permite crear una orden a un paciente."""

    serializer_class = serializers.OrdenSerializer
    queryset = Orden.objects.all()

    def post(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, pk=kwargs.get('pk'))
        response = super().post(request, *args, **kwargs)
        request.session.pop('cita', None)
        return response

    def get_serializer(self, *args, **kwargs):
        fields = [
            'id', 'institucion', 'plan', 'afiliacion', 'orden_link',
            'tipo_usuario', 'acompanante', 'servicios_realizar'
        ]
        expand = ['acompanante', 'servicios_realizar.sesiones']
        return super().get_serializer(fields=fields, expand=expand, *args, **kwargs)

    def perform_create(self, serializer):
        """Sobreescribe para setear el paciente."""

        serializer.save(paciente=self.paciente)


class HistoriasClinicasView(APIView):
    """Permite guardar la historia de un servicio."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/historias_clinicas.html'

    def get_historia(self, sesion):  # TODO: remove if not using
        """
        Retorna la historia de una sesion.
        """
        return getattr(sesion, 'historia', None)

    def get(self, request, pk):
        sesion = get_object_or_404(Sesion, pk=pk)
        paciente = sesion.servicio.orden.paciente

        serializer_paciente = PacienteSerializer(paciente, context={'request': request})
        paciente_json = JSONRenderer().render(serializer_paciente.data)

        historia = sesion.get_historia(force_instance=True)
        serializer_historia = HistoriaSerializer(historia, context={'request': request})

        historia_json = JSONRenderer().render(serializer_historia.data)
        return Response({'paciente': paciente_json, 'historia': historia_json, 'pk': pk})

    def post(self, request, pk):
        sesion = get_object_or_404(Sesion, pk=pk)
        historia = sesion.get_historia()
        serializer = HistoriaSerializer(historia, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(sesion=sesion)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED if historia is None else status.HTTP_202_ACCEPTED)
