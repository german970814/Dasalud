# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0009_auto_20170701_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acompanante',
            name='asistio',
            field=models.BooleanField(default=False, verbose_name='asistio con acompañante'),
        ),
    ]
