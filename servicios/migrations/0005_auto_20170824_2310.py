# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0004_auto_20170722_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarifaservicio',
            name='servicio',
        ),
        migrations.RemoveField(
            model_name='tarifaservicio',
            name='tarifa',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='tarifa',
        ),
        migrations.RemoveField(
            model_name='tarifa',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='tarifa',
            name='servicios',
        ),
        migrations.AddField(
            model_name='plan',
            name='servicios',
            field=models.ManyToManyField(related_name='planes', through='servicios.Tarifa', to='servicios.Servicio', verbose_name='servicios'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tarifas', to='servicios.Plan', verbose_name='plan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarifa',
            name='servicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tarifas', to='servicios.Servicio', verbose_name='servicio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarifa',
            name='valor',
            field=models.PositiveIntegerField(default=1000, verbose_name='valor'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TarifaServicio',
        ),
    ]
