from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='historias_clinicas/paciente_form.html'), name='crear_paciente'),
]