from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import ClienteSerializer, PlanSerializer, TarifaClienteSerializer
from .filters import PlanFilter
from .models import Cliente, Plan, Tarifa


class ListarEmpresasView(generics.ListAPIView):
    """Permite listar empresas."""

    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()

class ListarPlanesView(generics.ListAPIView):
    """Permite listar planes."""

    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    filter_class = PlanFilter

class ServiciosEmpresaView(generics.ListAPIView):
    """Permite listar los servicios de una empresa."""

    serializer_class = TarifaClienteSerializer

    def get_queryset(self):
        return Tarifa.objects.select_related('servicio').filter(plan=self.plan)
    
    def get(self, request, *args, **kwargs):
        self.plan = get_object_or_404(Plan, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)
