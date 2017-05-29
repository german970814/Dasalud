# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import pacientes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('globales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acompanante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asistio', models.BooleanField(verbose_name='acompañante')),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre completo')),
                ('direccion', models.CharField(max_length=200, verbose_name='dirección')),
                ('telefono', models.IntegerField(verbose_name='teléfono')),
            ],
            options={
                'verbose_name': 'acompañate',
                'verbose_name_plural': 'acompañates',
            },
            bases=(pacientes.models.ParentescoMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_orden', models.DateField(verbose_name='Fecha de la orden')),
                ('autorizacion', models.CharField(blank=True, max_length=50, verbose_name='autorización')),
                ('pendiente_autorizacion', models.BooleanField(default=False, verbose_name='Pendiente por autorización')),
                ('afiliacion', models.CharField(choices=[('C', 'Cotizante'), ('B', 'Beneficiario'), ('A', 'Subsidiado'), ('P', 'Particular'), ('V', 'Vinculado'), ('O', 'Otro')], max_length=1, verbose_name='afiliación')),
                ('tipo_usuario', models.CharField(choices=[('C', 'Contributivo'), ('A', 'Subsidiado'), ('V', 'Vinculado'), ('P', 'Particular'), ('O', 'Otro')], max_length=1, verbose_name='tipo de usuario')),
                ('anulada', models.BooleanField(default=False, verbose_name='anulada')),
                ('razon_anulacion', models.CharField(blank=True, max_length=200, verbose_name='razón de anulación')),
                ('forma_pago', models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta')], max_length=2, verbose_name='forma de pago')),
            ],
            options={
                'verbose_name': 'orden',
                'verbose_name_plural': 'ordenes',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=150, verbose_name='nombres')),
                ('apellidos', models.CharField(max_length=150, verbose_name='apellidos')),
                ('genero', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=1, verbose_name='género')),
                ('fecha_nacimiento', models.DateField(verbose_name='fecha de nacimiento')),
                ('fecha_ingreso', models.DateField(verbose_name='fecha de ingreso')),
                ('tipo_documento', models.CharField(choices=[('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería'), ('PA', 'Pasaporte'), ('RC', 'Registro civil'), ('TI', 'Tarjeta de identidad'), ('AN', 'Adulto sin identificar'), ('MN', 'Menor sin identificar'), ('NU', 'Número único de identificación')], max_length=2, verbose_name='tipo de documento')),
                ('numero_documento', models.CharField(max_length=20, unique=True, verbose_name='número de documento')),
                ('estado_civil', models.CharField(choices=[('V', 'Viudo'), ('C', 'Casado'), ('S', 'Soltero'), ('D', 'Divociado'), ('UL', 'Unión libre')], max_length=2, verbose_name='estado civil')),
                ('zona', models.CharField(choices=[('U', 'Urbano'), ('R', 'Rural')], max_length=1, verbose_name='zona')),
                ('direccion', models.CharField(max_length=200, verbose_name='dirección')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='telefono')),
                ('celular', models.IntegerField(blank=True, null=True, verbose_name='celular')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('grupo_sanguineo', models.CharField(blank=True, choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='grupo sanguineo')),
                ('grupo_etnico', models.CharField(blank=True, choices=[('D', 'Desplazado'), ('I', 'Indigena'), ('N', 'Negro'), ('O', 'Otro')], max_length=1, verbose_name='grupo etnico')),
                ('activo', models.BooleanField(default=True, verbose_name='activo')),
                ('foto', models.ImageField(blank=True, upload_to=pacientes.models.paciente_foto_path, verbose_name='foto')),
                ('firma', models.ImageField(blank=True, upload_to=pacientes.models.paciente_firma_path, verbose_name='firma')),
                ('nombre_responsable', models.CharField(max_length=300, verbose_name='nombre completo del responsable')),
                ('direccion_responsable', models.CharField(max_length=200, verbose_name='dirección del responsable')),
                ('telefono_responsable', models.IntegerField(blank=True, null=True, verbose_name='telefono del responsable')),
                ('identificacion_padre', models.CharField(blank=True, max_length=15, verbose_name='identificación del padre')),
                ('nombre_padre', models.CharField(blank=True, max_length=300, verbose_name='nombre completo del padre')),
                ('identificacion_madre', models.CharField(blank=True, max_length=15, verbose_name='identificación de la madre')),
                ('nombre_madre', models.CharField(blank=True, max_length=300, verbose_name='nombre completo de la madre')),
                ('lugar_nacimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pacientes_nacidos_en', to='globales.Poblado', verbose_name='nacio en')),
                ('lugar_residencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pacientes_viven_en', to='globales.Poblado', verbose_name='donde vive')),
                ('profesion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='globales.Profesion', verbose_name='profesión')),
            ],
            options={
                'verbose_name': 'paciente',
                'verbose_name_plural': 'pacientes',
            },
            bases=(pacientes.models.ParentescoMixin, models.Model),
        ),
        migrations.AddField(
            model_name='orden',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordenes', to='pacientes.Paciente', verbose_name='paciente'),
        ),
        migrations.AddField(
            model_name='acompanante',
            name='orden',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pacientes.Orden', verbose_name='orden'),
        ),
    ]
