from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^citas/$', views.CitasViews.as_view(), name='citas'),
    url(r'^horario-atencion/$', views.HorarioAtencionMedicosView.as_view(), name='horario-atencion'),
]