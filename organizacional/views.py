from django.shortcuts import render
from rest_framework import generics
from .serializers import EmpleadoSerializer
from .models import Empleado


class ListarMedicosView(generics.ListAPIView):
    """Permite listar planes."""

    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.filter(tipo=Empleado.MEDICO)
    filter_fields = ['instituciones']
