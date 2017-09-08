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

    def get_sesion(self, pk):
        self.sesion = get_object_or_404(Sesion, pk=pk)

    def get_historia(self):
        self.historia = self.sesion.get_historia(force_instance=True)
        return self.historia

    #  TODO ver si se hace metodo en modelo Sesion para que devuelva la historia
    def get_queryset(self):
        return self.get_historia().adjuntos.all()

    def get(self, request, sesion, *args, **kwargs):        
        self.get_sesion(sesion)
        return super().get(request, *args, **kwargs)

    def post(self, request, sesion, *args, **kwargs):
        self.get_sesion(sesion)
        self.get_historia()
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        from django.db import transaction
        with transaction.atomic():
            self.historia.save()
            serializer.save(historia=self.sesion.historia)

class AdjuntosHistoriaDestroyView(generics.DestroyAPIView):
    queryset = Adjunto.objects.all()
