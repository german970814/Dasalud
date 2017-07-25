from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AgendaView.as_view(), name='listar'),
    url(r'^citas/$', views.CitasView.as_view(), name='citas'),
    url(r'^horario-atencion/$', views.HorarioAtencionMedicosView.as_view(), name='horario-atencion'),
]