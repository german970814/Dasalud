from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AgendaView.as_view(), name='listar'),
    url(r'^citas/$', views.CitasView.as_view(), name='citas'),
    url(r'^citas/(?P<pk>\d+)$', views.CitaDetailView.as_view(), name='citas-detail'),
    url(r'^citas/multiple/$', views.CitasMultipleView.as_view(), name='citas-multiple'),
    url(r'^persona/buscar/$', views.BuscarPersonaView.as_view(), name='persona-search'),
    url(r'^horario-atencion/$', views.HorarioAtencionMedicosView.as_view(), name='horario-atencion'),
]