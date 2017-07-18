from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<servicio>\d+)/adjuntos/$', views.AdjuntosHistoriaView.as_view(), name='adjuntos'),
    url(r'^formatos/$', views.FormatoView.as_view()),
    url(r'^list/$', views.HistoriaView.as_view()),
]
