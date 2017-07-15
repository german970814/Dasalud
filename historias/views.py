from django.shortcuts import render
from rest_framework import generics
from .models import Historia, Formato
from . import serializers


class FormatoView(generics.ListCreateAPIView):

    serializer_class = serializers.FormatoSerializer
    queryset = Formato.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)
