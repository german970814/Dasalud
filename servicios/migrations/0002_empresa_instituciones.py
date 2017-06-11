# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20170606_2308'),
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='instituciones',
            field=models.ManyToManyField(related_name='empresas', to='organizacional.Institucion', verbose_name='instituciones'),
        ),
    ]
