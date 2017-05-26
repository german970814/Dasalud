# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(verbose_name='código')),
                ('nombre', models.CharField(max_length=250, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'departamentos',
                'verbose_name': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(verbose_name='código')),
                ('nombre', models.CharField(max_length=250, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'municipios',
                'verbose_name': 'municipio',
            },
        ),
        migrations.CreateModel(
            name='Poblado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(verbose_name='código')),
                ('nombre', models.CharField(max_length=250, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'poblados',
                'verbose_name': 'poblado',
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='nombre')),
                ('codigo', models.IntegerField(verbose_name='código')),
            ],
            options={
                'verbose_name_plural': 'profesiones',
                'verbose_name': 'profesión',
            },
        ),
    ]
