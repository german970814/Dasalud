from django.shortcuts import render
from rest_framework import generics, filters
from .serializers import CieSerializer
from .models import Cie


class ListarCiesView(generics.ListAPIView):
    """Permite listar los codigos internacianales de enfermedades."""

    serializer_class = CieSerializer
    queryset = Cie.objects.all()
    search_fields = ('nombre',)
    filter_backends = [filters.SearchFilter]