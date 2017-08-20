# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='creado el')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
    ]