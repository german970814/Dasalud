from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<sesion>\d+)/adjuntos/$', views.AdjuntosHistoriaView.as_view(), name='adjuntos'),
    url(r'^adjuntos/(?P<pk>\d+)/eliminar/$',
        views.AdjuntosHistoriaDestroyView.as_view(), name='adjuntos-eliminar'),
    url(r'^formatos/$', views.FormatoView.as_view()),
    url(r'^list/$', views.HistoriaView.as_view()),
]
