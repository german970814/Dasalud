# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_auto_20171011_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='procedencia',
            field=models.CharField(blank=True, choices=[('IG', 'Instagram'), ('FB', 'Facebook'), ('IN', 'Internet'), ('R', 'Referido')], max_length=2, verbose_name='como se entero'),
        ),
    ]