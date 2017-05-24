from django.shortcuts import redirect, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .serializers import PacienteSerializer


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
    template_name = 'historias_clinicas/lista_pacientes.html'

    def get(self, request):
        serializer = PacienteSerializer(Paciente.objects.all(), many=True, context={'request': None})
        pacientes = JSONRenderer().render(serializer.data)
        return Response({'pacientes': pacientes, 'total_pacientes': len(serializer.data)})


class CrearPacienteView(APIView):
    """Permite crear un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'historias_clinicas/paciente_form.html'

    def get(self, request):
        serializer = PacienteSerializer(context={'request': None})
        return Response({'serializer': serializer})
    
    def post(self, request):
        serializer = PacienteSerializer(data=request.data, context={'request': None})
        if serializer.is_valid():
            serializer.save()
            return redirect('historias_clinicas:listar_pacientes')
        return Response({'serializer': serializer})


class EditarPacienteView(APIView):
    """Permite editar un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'historias_clinicas/paciente_form.html'

    def get(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, context={'request': None})
        return Response({'serializer': serializer})
    
    def post(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        serializer = PacienteSerializer(paciente, data=request.data, context={'request': None})
        if serializer.is_valid():
            serializer.save()
            return redirect('historias_clinicas:listar_pacientes')
        return Response({'serializer': serializer})



