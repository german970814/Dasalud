import waffle
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from common.serializers import PrimaryKeyGlobalIDMixin
from common.schema import BaseNode
from agenda.models import Cita, Persona, HorarioAtencion
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    graph_id = serializers.SerializerMethodField()
    edit_link = serializers.SerializerMethodField()
    ordenes_link = serializers.SerializerMethodField()

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento',
            'numero_documento', 'genero', 'estado_civil', 'fecha_nacimiento', 'zona', 'direccion', 'telefono',
            'celular', 'email', 'grupo_sanguineo', 'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia',
            'activo', 'fecha_ingreso', 'nombre_responsable', 'direccion_responsable', 'telefono_responsable',
            'edit_link', 'ordenes_link', 'identificacion_padre', 'nombre_padre', 'identificacion_madre',
            'nombre_madre', 'foto', 'firma', 'graph_id', 'procedencia'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = models.Paciente.URBANO
        self.fields['grupo_etnico'].initial = models.Paciente.OTRO
        self.fields['foto'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})
        self.fields['firma'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})

    def get_graph_id(self, obj):
        return BaseNode.to_global_id('Paciente', obj.id)

    def get_ordenes_link(self, obj):
        request = self.context.get('request', None)
        if request and not request.user.has_perm('pacientes.add_orden'):
            return None

        return reverse('pacientes:ordenes-nueva', kwargs={'pk': obj.pk})

    def get_edit_link(self, obj):
        request = self.context.get('request', None)
        if request and not request.user.has_perm('pacientes.change_paciente'):
            return None

        return reverse('pacientes:editar', kwargs={'pk': obj.pk})


class AcompananteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo acompanante."""

    class Meta:
        model = models.Acompanante
        fields = ['asistio', 'nombre', 'direccion', 'telefono']

    # TODO validar cuando asistio es True


class OrdenSerializer(PrimaryKeyGlobalIDMixin, FlexFieldsModelSerializer):
    """Serializer para el modelo Orden."""

    cliente = serializers.SerializerMethodField()
    orden_link = serializers.SerializerMethodField()

    class Meta:
        model = models.Orden
        fields = [
            'id', 'fecha_orden', 'institucion', 'plan', 'cliente', 'afiliacion', 'tipo_usuario',
            'anulada', 'razon_anulacion', 'servicios_realizar', 'paciente', 'orden_link'
        ]

    expandable_fields = {
        'paciente': (PacienteSerializer, {'source': 'paciente'}),
        'acompanante': (AcompananteSerializer, {'source': 'acompanante'}),
        'servicios_realizar': ('pacientes.ServicioRealizarSerializer', {
            'source': 'servicios_realizar', 'many': True, 'fields': [
               'id' ,'servicio', 'coopago', 'valor', 'numero_sesiones', 'sesiones'
            ]
        })
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['afiliacion'].initial = models.Orden.PARTICULAR
        self.fields['tipo_usuario'].initial = models.Orden.PARTICULAR
        self.fields['plan'].label = 'Entidad'

    def create(self, validated_data):  #  TODO ver si se crea metodo create en manager de Orden
        servicios_data = validated_data.pop('servicios_realizar')
        acompanante_data = validated_data.pop('acompanante')

        with transaction.atomic():
            orden = super().create(validated_data)
            models.Acompanante.objects.create(orden=orden, **acompanante_data)
            for servicio_data in servicios_data:
                sesiones_data = servicio_data.pop('sesiones')
                servicio = models.ServicioRealizar.objects.create(orden=orden, **servicio_data)
                for sesion_data in sesiones_data:
                    sesion = models.Sesion.objects.create(servicio=servicio, **sesion_data)

                    if waffle.switch_is_active('citas'):
                        cita = sesion_data.get('cita', None)
                        if cita:
                            cita.sesion = sesion
                            cita.estado = sesion.estado
                            cita.save()
                        else:
                            self.crear_cita(sesion, servicio.servicio, orden.paciente)
            
            # raise ValueError('force error')
            return orden
    
    def update(self, instance, validated_data):
        servicios_data = validated_data.pop('servicios_realizar')
        acompanante_data = validated_data.pop('acompanante')

        with transaction.atomic():
            instance.update(**validated_data)
            instance.acompanante.update(**acompanante_data)

            for servicio_data in servicios_data:
                sesiones_data = servicio_data.pop('sesiones')
                models.ServicioRealizar.objects.get(id=servicio_data.pop('id')).update(**servicio_data)
                for sesion_data in sesiones_data:
                    sesion = models.Sesion.objects.get(id=sesion_data.pop('id')).update(**sesion_data)

            # raise ValueError('error force ')
        return instance

    def get_cliente(self, obj):
        """
        :returns:
            Nombre de la cliente cliente con la cual se encuentra asociada la orden.
        """

        return str(obj.plan.cliente)

    def get_orden_link(self, obj):
        return reverse('pacientes:ordenes-detalle', kwargs={'paciente': obj.paciente_id, 'pk': obj.id})

    def crear_cita(self, sesion, servicio, paciente):
        persona = Persona.objects.get(numero_documento=paciente.numero_documento)
        horario = HorarioAtencion.objects.get(medico=sesion.medico_id, sucursal=sesion.sucursal_id, start=sesion.fecha)
        Cita.objects.create(sesion=sesion, estado=sesion.estado, servicio=servicio, paciente=persona, horario=horario)

class ServicioRealizarSerializer(PrimaryKeyGlobalIDMixin, FlexFieldsModelSerializer):
    """Serializer para el modelo ServicioRealizar."""

    id = serializers.IntegerField(required=False, read_only=False)

    class Meta:
        model = models.ServicioRealizar
        fields = ['id', 'orden', 'servicio', 'numero_sesiones', 'valor', 'coopago']
    
    expandable_fields = {
        'sesiones': ('pacientes.SesionSerializer', {'source': 'sesiones', 'many': True, 'fields': [
            'id', 'fecha', 'medico', 'sucursal', 'cita', 'autorizacion', 'fecha_autorizacion', 'estado'
        ]})
    }


class SesionSerializer(PrimaryKeyGlobalIDMixin, FlexFieldsModelSerializer):
    """Serializer para el modelo Sesion."""

    id = serializers.IntegerField(required=False, read_only=False)

    class Meta:
        model = models.Sesion
        fields = [
            'id', 'fecha', 'medico', 'servicio', 'sucursal', 'cita', 'autorizacion', 'fecha_autorizacion', 'estado'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cita'].required = False
    
    def validate(self, data):
        """
        Valida que el medico tenga un horario disponible  en la sucursal para la fecha escogido.
        Solo usado cuando el switch 'citas' se encuentra activo.
        """

        if waffle.switch_is_active('citas'):
            hay_horario = HorarioAtencion.objects.filter(
                    medico=data['medico'], sucursal=data['sucursal'], start=data['fecha']
                ).exists()
            
            if not hay_horario:
                raise serializers.ValidationError({'fecha': 'No hay horario de atención disponible.'})
            
        return data
                

