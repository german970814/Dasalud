from django.shortcuts import render
from rest_framework import generics
from .serializers import EmpleadoSerializer, SucursalSerializer
from .models import Empleado, Sucursal


class ListarMedicosView(generics.ListAPIView):
    """Permite listar los medicos."""

    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.medicos()
    filter_fields = ['instituciones']


class ListarSucursalesView(generics.ListAPIView):
    """Permite listar las sucursales."""

    serializer_class = SucursalSerializer
    queryset = Sucursal.objects.all()
