from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from pacientes.serializers import ServicioOrdenSerializer


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
