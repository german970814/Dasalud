import waffle
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from common.serializers import PrimaryKeyGlobalIDMixin
from common.schema import BaseNode
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    edit_link = serializers.HyperlinkedIdentityField(view_name='pacientes:editar')
    ordenes_link = serializers.HyperlinkedIdentityField(view_name='pacientes:ordenes-nueva')
    graph_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento',
            'numero_documento', 'genero', 'estado_civil', 'fecha_nacimiento', 'zona', 'direccion', 'telefono',
            'celular', 'email', 'grupo_sanguineo', 'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia',
            'activo', 'fecha_ingreso', 'nombre_responsable', 'direccion_responsable', 'telefono_responsable',
            'edit_link', 'ordenes_link', 'identificacion_padre', 'nombre_padre', 'identificacion_madre',
            'nombre_madre', 'foto', 'firma', 'graph_id'
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

    # TODO validar campos

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
                            cita.save()
                        else:
                            self.crear_cita(sesion, servicio.servicio, orden.paciente)
            
            # raise ValueError
            return orden

    def get_cliente(self, obj):
        """
        :returns:
            Nombre de la cliente cliente con la cual se encuentra asociada la orden.
        """

        return str(obj.plan.cliente)

    def get_orden_link(self, obj):
        return reverse('pacientes:ordenes-detalle', kwargs={'paciente': obj.paciente_id, 'pk': obj.id})

    def crear_cita(self, sesion, servicio, paciente):
        from agenda.models import Cita, Persona, HorarioAtencion
        persona = Persona.objects.get(numero_documento=paciente.numero_documento)
        horario = HorarioAtencion.objects.get(medico=sesion.medico_id, sucursal=sesion.sucursal_id, start=sesion.fecha)
        Cita.objects.create(sesion=sesion, estado=Cita.NO_CONFIRMADA, servicio=servicio, paciente=persona, horario=horario)

class ServicioRealizarSerializer(PrimaryKeyGlobalIDMixin, FlexFieldsModelSerializer):
    """Serializer para el modelo ServicioRealizar."""

    class Meta:
        model = models.ServicioRealizar
        fields = ['id', 'orden', 'servicio', 'numero_sesiones', 'valor', 'coopago']
    
    expandable_fields = {
        'sesiones': ('pacientes.SesionSerializer', {'source': 'sesiones', 'many': True, 'fields': [
            'id', 'fecha', 'medico', 'sucursal', 'cita'
        ]})
    }


class SesionSerializer(PrimaryKeyGlobalIDMixin, FlexFieldsModelSerializer):
    """Serializer para el modelo Sesion."""

    class Meta:
        model = models.Sesion
        fields = [
            'id', 'fecha', 'medico', 'servicio', 'sucursal', 'cita', 'autorizacion', 'fecha_autorizacion', 'estado'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cita'].required = False


class ServicioOrdenSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo ServicioOrden."""

    historias_link = serializers.HyperlinkedIdentityField(view_name='pacientes:historias')
    servicio_nombre = serializers.StringRelatedField(source='servicio')

    class Meta:
        model = models.ServicioOrden
        fields = ['medico', 'servicio', 'tipo_pago', 'valor', 'descuento', 'orden', 'historias_link', 'servicio_nombre']

    expandable_fields = {
        'orden': (OrdenSerializer, {'source': 'orden'})
    }
