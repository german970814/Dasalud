from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _lazy
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .serializers import PacienteSerializer, OrdenSerializer, AcompananteSerializer, ServicioOrdenSerializer


from rest_framework import generics
class PacientesList(generics.ListAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = None
        return context


class ListarPacientesView(generics.ListCreateAPIView):
    """Lista los pacientes."""

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'pacientes/lista_pacientes.html'
    serializer_class = PacienteSerializer

    def get(self, request):
        serializer = PacienteSerializer(Paciente.objects.all(), many=True, context={'request': None})
        pacientes = JSONRenderer().render(serializer.data)
        return Response({'pacientes': pacientes, 'total_pacientes': len(serializer.data)})


class CrearPacienteView(APIView):
    """Permite crear un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/paciente_form.html'
    VERBO = _lazy('Crear')

    def get(self, request):
        paciente_s = PacienteSerializer(context={'request': None})
        orden_s = OrdenSerializer()
        acompanante_s = AcompananteSerializer()
        servicios_s = ServicioOrdenSerializer()
        return Response({
            'paciente_s': paciente_s, 'orden_s': orden_s, 'servicios_s': servicios_s,
            'acompanante_s': acompanante_s, 'VERBO': self.VERBO
        })


class EditarPacienteView(APIView):
    """Permite editar un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/paciente_form.html'
    VERBO = _lazy('Editar')

    def get(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, context={'request': None})
        return Response({'serializer': serializer, 'VERBO': self.VERBO})
    
    def post(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, data=request.data, context={'request': None})
        if serializer.is_valid():
            serializer.save()
            return redirect('pacientes:listar_pacientes')
        return Response({'serializer': serializer, 'VERBO': self.VERBO})


class CrearOrdenView(APIView):
    """Permite crear una orden a un paciente."""

    renderer_class = [JSONRenderer]

    def post(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        return Response()



