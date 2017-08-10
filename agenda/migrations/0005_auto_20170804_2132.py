# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_auto_20170724_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, verbose_name='dirección'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='agenda.HorarioAtencion', verbose_name='horario'),
        ),
    ]
