from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import EmpresaSerializer, PlanSerializer, TarifaServiciosEmpresaSerializer
from .filters import PlanFilter
from .models import Empresa, Plan, TarifaServicio


class ListarEmpresasView(generics.ListAPIView):
    """Permite listar empresas."""

    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()

class ListarPlanesView(generics.ListAPIView):
    """Permite listar planes."""

    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    filter_class = PlanFilter

class ServiciosEmpresaView(generics.ListAPIView):
    """Permite listar los servicios de una empresa."""

    serializer_class = TarifaServiciosEmpresaSerializer

    def get_queryset(self):
        return TarifaServicio.objects.select_related('servicio').filter(tarifa=self.plan.tarifa_id)
    
    def get(self, request, *args, **kwargs):
        self.plan = get_object_or_404(Plan, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)