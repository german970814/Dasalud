from django.conf.urls import url
from django.contrib import admin
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.ListarPacientesView.as_view(), name='listar'),
    url(r'^nuevo$', views.CrearPacienteView.as_view(), name='crear'),
    url(r'^(?P<pk>\d+)$', views.EditarPacienteView.as_view(), name='editar'),
    url(r'^(?P<pk>\d+)/ordenes/$', views.CrearOrdenView.as_view(), name='crear_orden'),



    url(r'^list/$', views.PacientesList.as_view()),
]