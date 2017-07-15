from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^formatos/$', views.FormatoView.as_view()),
]
