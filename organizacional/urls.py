from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^medicos/$', views.ListarMedicosView.as_view(), name='medicos'),
    url(r'^sucursales/$', views.ListarSucursalesView.as_view(), name='sucursales'),
]