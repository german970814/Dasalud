from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^empresas/$', views.ListarEmpresasView.as_view(), name='empresas'),
    url(r'^empresas/(?P<pk>\d+)/servicios/$', views.ServiciosEmpresaView.as_view(), name='empresas_servicios'),
    url(r'^planes/$', views.ListarPlanesView.as_view(), name='planes')
]