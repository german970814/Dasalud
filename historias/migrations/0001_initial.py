# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 00:18
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0009_auto_20170701_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('formato', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'verbose_name_plural': 'formatos',
                'verbose_name': 'formato',
            },
        ),
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historia', django.contrib.postgres.fields.jsonb.JSONField()),
                ('terminada', models.BooleanField(default=False)),
                ('servicio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pacientes.ServicioOrden', verbose_name='servicio')),
            ],
            options={
                'verbose_name_plural': 'historias',
                'verbose_name': 'historia',
            },
        ),
    ]