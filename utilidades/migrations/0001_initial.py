# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='nombre')),
                ('codigo', models.CharField(max_length=3, verbose_name='código')),
            ],
            options={
                'verbose_name_plural': 'profesiones',
                'verbose_name': 'profesión',
            },
        ),
    ]
