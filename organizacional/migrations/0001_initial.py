# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 03:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import organizacional.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('globales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100, verbose_name='nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='apellidos')),
                ('cedula', models.PositiveIntegerField(verbose_name='cédula')),
                ('activo', models.BooleanField(default=True, verbose_name='activo')),
                ('registro_medico', models.CharField(blank=True, max_length=100, verbose_name='registro medico')),
                ('firma', models.ImageField(blank=True, upload_to=organizacional.models.empleado_firma_path, verbose_name='firma')),
                ('tipo', models.CharField(choices=[('M', 'medicos'), ('A', 'administrativos')], max_length=2, verbose_name='tipo')),
            ],
            options={
                'verbose_name_plural': 'empleados',
                'verbose_name': 'empleado',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('razon_social', models.CharField(max_length=100, verbose_name='razón social')),
                ('tipo_documento', models.CharField(choices=[('NI', 'NIT'), ('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería')], max_length=2, verbose_name='tipo de documento')),
                ('identificacion', models.CharField(max_length=50, verbose_name='identificación')),
                ('codigo', models.CharField(blank=True, max_length=50, verbose_name='código')),
                ('direccion', models.CharField(max_length=100, verbose_name='dirección')),
                ('telefono', models.PositiveIntegerField(blank=True, null=True, verbose_name='telefono')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instituciones', to='globales.Poblado', verbose_name='ciudad')),
            ],
            options={
                'verbose_name_plural': 'instituciones',
                'verbose_name': 'institución',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('direccion', models.CharField(blank=True, max_length=100, verbose_name='dirección')),
                ('telefono', models.PositiveIntegerField(blank=True, null=True, verbose_name='telefono')),
            ],
            options={
                'verbose_name_plural': 'sucursales',
                'verbose_name': 'sucursal',
            },
        ),
        migrations.AddField(
            model_name='empleado',
            name='instituciones',
            field=models.ManyToManyField(related_name='empleados', to='organizacional.Institucion', verbose_name='instituciones'),
        ),
    ]
