from django.conf.urls import url
from django.contrib import admin
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.ListarPacientesView.as_view(), name='listar'),
    url(r'^nuevo$', views.CrearPacienteView.as_view(), name='crear'),
    url(r'^busqueda/$', views.BucarPacientesView.as_view(), name='busqueda'),
    url(r'^(?P<pk>\d+)$', views.PacienteDetalleView.as_view(), name='detalle'),
    url(r'^(?P<pk>\d+)/editar/$', views.EditarPacienteView.as_view(), name='editar'),
    url(r'^(?P<pk>\d+)/ordenes/$', views.OrdenesPacienteView.as_view(), name='ordenes'),
    url(r'^(?P<pk>\d+)/ordenes/nueva/$', views.CrearOrdenView.as_view(), name='ordenes-nueva'),



    url(r'^list/$', views.PacientesList.as_view()),
    url(r'^ordenes/$', views.OrdenesList.as_view()),
]