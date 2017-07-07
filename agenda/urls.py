from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^citas/$', views.CitasViews.as_view(), name='citas'),
]