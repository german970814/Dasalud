from django.conf.urls import url
from django.contrib import admin
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^pacientes/$', views.ListarPacientesView.as_view(), name='listar_pacientes'),
    url(r'^pacientes/nuevo$', views.CrearPacienteView.as_view(), name='crear_paciente'),
]