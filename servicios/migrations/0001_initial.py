# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 03:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('globales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('razon_social', models.CharField(max_length=200, verbose_name='razón social')),
                ('nit', models.CharField(max_length=50, verbose_name='nit')),
                ('direccion', models.CharField(blank=True, max_length=100, verbose_name='dirección')),
                ('telefono', models.PositiveIntegerField(blank=True, null=True, verbose_name='telefono')),
                ('codigo', models.CharField(blank=True, max_length=100, verbose_name='código')),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to='globales.Poblado', verbose_name='ciudad')),
            ],
            options={
                'verbose_name_plural': 'empresas',
                'verbose_name': 'empresa',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='plan')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planes', to='servicios.Empresa', verbose_name='empresa')),
            ],
            options={
                'verbose_name_plural': 'planes',
                'verbose_name': 'plan',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('codigo', models.CharField(max_length=100, verbose_name='código')),
                ('abreviatura', models.CharField(max_length=100, verbose_name='abreviatura')),
                ('cups', models.CharField(blank=True, max_length=100, verbose_name='cups')),
                ('costo', models.PositiveIntegerField(blank=True, null=True, verbose_name='costo')),
            ],
            options={
                'verbose_name_plural': 'servicios',
                'verbose_name': 'servicio',
            },
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'tarifas',
                'verbose_name': 'tarifa',
            },
        ),
        migrations.CreateModel(
            name='TarifaServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveIntegerField(verbose_name='valor')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifas_servicio', to='servicios.Servicio')),
                ('tarifa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifas_servicio', to='servicios.Tarifa')),
            ],
            options={
                'verbose_name_plural': 'tarifas por servicio',
                'verbose_name': 'tarifa por servicio',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'tipos',
                'verbose_name': 'tipo',
            },
        ),
        migrations.AddField(
            model_name='tarifa',
            name='servicios',
            field=models.ManyToManyField(related_name='tarifas', through='servicios.TarifaServicio', to='servicios.Servicio', verbose_name='servicios'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios', to='servicios.Tipo', verbose_name='tipo'),
        ),
        migrations.AddField(
            model_name='plan',
            name='tarifa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planes', to='servicios.Tarifa', verbose_name='tarifa'),
        ),
    ]