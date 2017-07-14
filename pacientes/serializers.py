from django.db import transaction
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from . import models


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo paciente."""

    edit_link = serializers.HyperlinkedIdentityField(view_name='pacientes:editar')
    ordenes_link = serializers.HyperlinkedIdentityField(view_name='pacientes:ordenes-nueva')

    class Meta:
        model = models.Paciente
        fields = [
            'id', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'estado_civil',
            'fecha_nacimiento', 'zona', 'direccion', 'telefono', 'celular', 'email', 'grupo_sanguineo',
            'grupo_etnico', 'profesion', 'lugar_nacimiento', 'lugar_residencia', 'activo', 'fecha_ingreso',
            'nombre_responsable', 'direccion_responsable', 'telefono_responsable', 'edit_link', 'ordenes_link',
            'identificacion_padre', 'nombre_padre', 'identificacion_madre', 'nombre_madre', 'foto', 'firma'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].initial = True
        self.fields['zona'].initial = models.Paciente.URBANO
        self.fields['grupo_etnico'].initial = models.Paciente.OTRO
        self.fields['foto'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})
        self.fields['firma'].style.update({'attrs': 'no-auto max-files=1 accept=image/*'})


class AcompananteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo acompanante."""

    class Meta:
        model = models.Acompanante
        fields = ['asistio', 'nombre', 'direccion', 'telefono']

    # TODO validar cuando asistio es True


class OrdenSerializer(FlexFieldsModelSerializer):
    """Serializer para el modelo Orden."""

    empresa = serializers.SerializerMethodField()

    class Meta:
        model = models.Orden
        fields = [
            'id', 'fecha_orden', 'sucursal', 'autorizacion', 'pendiente_autorizacion', 'institucion', 'plan', 'empresa',
            'afiliacion', 'tipo_usuario', 'forma_pago', 'anulada', 'razon_anulacion', 'servicios', 'paciente'
        ]

    expandable_fields = {
        'paciente': (PacienteSerializer, {'source': 'paciente'}),
        'acompanante': (AcompananteSerializer, {'source': 'acompanante'}),
        'servicios': ('pacientes.ServicioOrdenSerializer', {
            'source': 'servicios_orden', 'many': True, 'fields': [
                'medico', 'servicio', 'tipo_pago', 'valor', 'descuento', 'historias_link'
            ]
        })
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['afiliacion'].initial = models.Orden.PARTICULAR
        self.fields['tipo_usuario'].initial = models.Orden.PARTICULAR

    # TODO validar campos

    def create(self, validated_data):  #  TODO ver si se crea metodo create en manager de Orden
        servicios_data = validated_data.pop('servicios_orden')
        acompanante_data = validated_data.pop('acompanante')

        with transaction.atomic():
            orden = super().create(validated_data)
            models.Acompanante.objects.create(orden=orden, **acompanante_data)
            for servicio_data in servicios_data:
                models.ServicioOrden.objects.create(orden=orden, **servicio_data)
            return orden

    def get_empresa(self, obj):
        """
        :returns:
            Nombre de la empresa cliente con la cual se encuentra asociada la orden.
        """

        return str(obj.plan.empresa)


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
