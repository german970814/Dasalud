from django.shortcuts import render
from rest_framework import generics
from .serializers import EmpresaSerializer, PlanSerializer
from .filters import PlanFilter
from .models import Empresa, Plan


class ListarEmpresasView(generics.ListAPIView):
    """Permite listar empresas."""

    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()

class ListarPlanesView(generics.ListAPIView):
    """Permite listar planes."""

    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    filter_class = PlanFilter

