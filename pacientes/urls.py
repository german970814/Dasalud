from django.conf.urls import url
from django.contrib import admin
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^pacientes/$', views.ListarPacientesView.as_view(), name='listar'),
    url(r'^pacientes/nuevo$', views.CrearPacienteView.as_view(), name='crear'),
    url(r'^pacientes/(?P<pk>\d+)$', views.EditarPacienteView.as_view(), name='editar'),



    url(r'^pacientes-list/$', views.PacientesList.as_view()),
]