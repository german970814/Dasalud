# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='servicios',
            field=models.ManyToManyField(related_name='ordenes', through='pacientes.ServicioRealizar', to='servicios.Servicio', verbose_name='servicios'),
        ),
    ]
