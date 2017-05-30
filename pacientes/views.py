from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _lazy
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .serializers import PacienteSerializer, OrdenSerializer, AcompananteSerializer


from rest_framework import generics
class PacientesList(generics.ListAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = None
        return context


class ListarPacientesView(APIView):
    """Lista los pacientes."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pacientes/lista_pacientes.html'

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
        return Response({'paciente_s': paciente_s, 'orden_s': orden_s, 'acompanante_s': acompanante_s, 'VERBO': self.VERBO})
    
    def post(self, request):
        orden_s = OrdenSerializer(data=request.data)
        acompanante_s = AcompananteSerializer(data=request.data)
        paciente_s = PacienteSerializer(data=request.data, context={'request': None})
        acompanante_v = acompanante_s.is_valid()
        paciente_v = paciente_s.is_valid()
        orden_v = orden_s.is_valid()

        if paciente_v and orden_v and acompanante_v:
            # paciente.save()
            return redirect('pacientes:listar_pacientes')
        print(".........................", paciente_s.errors, orden_s.errors, acompanante_s.errors)
        print(".........................", paciente_s.data, orden_s.data, acompanante_s.data)
        return Response({'paciente_s': paciente_s, 'orden_s': orden_s, 'acompanante_s': acompanante_s, 'VERBO': self.VERBO})


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



