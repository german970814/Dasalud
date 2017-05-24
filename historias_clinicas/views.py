from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .serializers import PacienteSerializer


class ListarPacientesView(APIView):
    """Lista los pacientes."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'historias_clinicas/lista_pacientes.html'

    def get(self, request):
        serializer = PacienteSerializer(Paciente.objects.all(), many=True)
        pacientes = JSONRenderer().render(serializer.data)
        return Response({'pacientes': pacientes, 'total_pacientes': len(serializer.data)})


class CrearPacienteView(APIView):
    """Permite crear un paciente."""

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'historias_clinicas/paciente_form.html'

    def get(self, request):
        serializer = PacienteSerializer()
        return Response({'serializer': serializer})
    
    def post(self, request):
        serializer = PacienteSerializer(data=request.data)
        serializer.is_valid()
        return Response({'serializer': serializer})



