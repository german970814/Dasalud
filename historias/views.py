from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from pacientes.models import ServicioOrden
from .models import Historia, Formato, Adjunto
from . import serializers


class FormatoView(generics.ListCreateAPIView):

    serializer_class = serializers.FormatoSerializer
    queryset = Formato.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class HistoriaView(generics.ListCreateAPIView):

    serializer_class = serializers.HistoriaSerializer
    queryset = Historia.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdjuntosHistoriaView(generics.ListCreateAPIView):
    """Permite adjuntar archivos a una historia clinica."""

    serializer_class = serializers.AdjuntoSerializer
    queryset = Adjunto.objects.all()

    def get_servicio(self, servicio):
        self.servicio = get_object_or_404(ServicioOrden, pk=servicio)

    #  TODO ver si se hace metodo en modelo ServicioOrden para que devuelva la historia
    def get_queryset(self):
        return self.servicio.historia.adjuntos.all()

    def get(self, request, servicio, *args, **kwargs):        
        self.get_servicio(servicio)
        return super().get(request, *args, **kwargs)

    def post(self, request, servicio, *args, **kwargs):
        self.get_servicio(servicio)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(historia=self.servicio.historia)