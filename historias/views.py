from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from pacientes.models import Sesion
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

    def get_sesion(self, sesion):
        self.sesion = get_object_or_404(Sesion, pk=sesion)

    #  TODO ver si se hace metodo en modelo sesionOrden para que devuelva la historia
    def get_queryset(self):
        return self.sesion.historia.adjuntos.all()

    def get(self, request, sesion, *args, **kwargs):        
        self.get_sesion(sesion)
        return super().get(request, *args, **kwargs)

    def post(self, request, sesion, *args, **kwargs):
        self.get_sesion(sesion)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(historia=self.sesion.historia)