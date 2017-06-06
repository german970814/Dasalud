from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


class ParentescoMixin(object):
    """Mixin para los parentescos de un paciente."""

    TIO = 'T'
    OTRO = 'O'
    HIJO = 'I'
    PADRE = 'P'
    MADRE = 'M'
    AMIGO = 'AM'
    ABUELO = 'A'
    PRIMO = 'PR'
    HERMANO = 'H'
    CONYUGUE = 'C'
    PARENTESCOS = (
        (PADRE, _lazy('Padre')),
        (MADRE, _lazy('Madre')),
        (HERMANO, _lazy('Hermano')),
        (HIJO, _lazy('Hijo')),
        (ABUELO, _lazy('Abuelo')),
        (TIO, _lazy('Tio')),
        (PRIMO, _lazy('Primo')),
        (CONYUGUE, _lazy('Conyugue')),
        (AMIGO, _lazy('Amigo')),
        (OTRO, _lazy('Otro'))
    )

    parentesco = models.CharField(_lazy('parentesco'), max_length=3, choices=PARENTESCOS)

    class Meta:
        abstract = True

def paciente_foto_path(instance, filename):
    return 'paciente_{0}/foto_{1}'.format(instance.pk, filename)


def paciente_firma_path(instance, filename):
    return 'paciente_{0}/firma_{1}'.format(instance.pk, filename)


class Paciente(ParentescoMixin, models.Model):
    """Modelo para guardar la información de un paciente."""

    FEMENINO = 'F'
    MASCULINO = 'M'
    GENEROS = (
        (FEMENINO, _lazy('Femenino')),
        (MASCULINO, _lazy('Masculino'))
    )

    MENOR_NN = 'MN'
    ADULTO_NN = 'AN'
    PASAPORTE = 'PA'
    REGISTRO_CIVIL = 'RC'
    NUMERO_UNICO_ID = 'NU'
    CEDULA_CIUDADANIA = 'CC'
    TARJETA_IDENTIDAD = 'TI'
    CEDULA_EXTRANJERIA = 'CE'
    TIPO_DOCUMENTOS = (
        (CEDULA_CIUDADANIA, _lazy('Cédula de ciudadanía')),
        (CEDULA_EXTRANJERIA, _lazy('Cédula de extranjería')),
        (PASAPORTE, _lazy('Pasaporte')),
        (REGISTRO_CIVIL, _lazy('Registro civil')),
        (TARJETA_IDENTIDAD, _lazy('Tarjeta de identidad')),
        (ADULTO_NN, _lazy('Adulto sin identificar')),
        (MENOR_NN, _lazy('Menor sin identificar')),
        (NUMERO_UNICO_ID, 'Número único de identificación')
    )

    VIUDO = 'V'
    CASADO = 'C'
    SOLTERO = 'S'
    DIVORCIADO = 'D'
    UNION_LIBRE = 'UL'
    ESTADOS_CIVILES = (
        (VIUDO, _lazy('Viudo')),
        (CASADO, _lazy('Casado')),
        (SOLTERO, _lazy('Soltero')),
        (DIVORCIADO, _lazy('Divociado')),
        (UNION_LIBRE, _lazy('Unión libre'))
    )

    RURAL = 'R'
    URBANO = 'U'
    ZONAS = (
        (URBANO, _lazy('Urbano')),
        (RURAL, _lazy('Rural'))
    )

    O_POSITIVO = 'O+'
    O_NEGATIVO = 'O-'
    A_POSITIVO = 'A+'
    A_NEGATIVO = 'A-'
    B_POSITIVO = 'B+'
    B_NEGATIVO = 'B-'
    AB_POSITIVO = 'AB+'
    AB_NEGATIVO = 'AB-'
    GRUPOS_SANGUINEOS = (
        (O_NEGATIVO, O_NEGATIVO),
        (O_POSITIVO, O_POSITIVO),
        (A_NEGATIVO, A_NEGATIVO),
        (A_POSITIVO, A_POSITIVO),
        (B_NEGATIVO, B_NEGATIVO),
        (B_POSITIVO, B_POSITIVO),
        (AB_NEGATIVO, AB_NEGATIVO),
        (AB_POSITIVO, AB_POSITIVO),
    )

    OTRO = 'O'
    NEGRO = 'N'
    INDIGENA = 'I'
    DESPLAZADO = 'D'
    GRUPOS_ETNICOS = (
        (DESPLAZADO, _lazy('Desplazado')),
        (INDIGENA, _lazy('Indigena')),
        (NEGRO, _lazy('Negro')),
        (OTRO, _lazy('Otro'))
    )

    nombres = models.CharField(_lazy('nombres'), max_length=150)
    apellidos = models.CharField(_lazy('apellidos'), max_length=150)
    genero = models.CharField(_lazy('género'), max_length=1, choices=GENEROS)
    fecha_nacimiento = models.DateField(_lazy('fecha de nacimiento'))
    fecha_ingreso = models.DateField(_lazy('fecha de ingreso'))
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    numero_documento = models.CharField(_lazy('número de documento'), max_length=20, unique=True)
    estado_civil = models.CharField(_lazy('estado civil'), max_length=2, choices=ESTADOS_CIVILES)
    zona = models.CharField(_lazy('zona'), max_length=1, choices=ZONAS)
    direccion = models.CharField(_lazy('dirección'), max_length=200)
    telefono = models.PositiveIntegerField(_lazy('telefono'), null=True, blank=True)
    celular = models.IntegerField(_lazy('celular'), null=True, blank=True)
    email = models.EmailField(_lazy('email'))
    grupo_sanguineo = models.CharField(_lazy('grupo sanguineo'), max_length=3, choices=GRUPOS_SANGUINEOS, blank=True)
    grupo_etnico = models.CharField(_lazy('grupo etnico'), max_length=1, choices=GRUPOS_ETNICOS, blank=True)
    activo = models.BooleanField(_lazy('activo'), default=True)
    profesion = models.ForeignKey('globales.Profesion', related_name='pacientes', verbose_name=_lazy('profesión'),  null=True, blank=True)
    lugar_nacimiento = models.ForeignKey('globales.Poblado', related_name='pacientes_nacidos_en', verbose_name=_lazy('nacio en'))
    lugar_residencia = models.ForeignKey('globales.Poblado', related_name='pacientes_viven_en', verbose_name=_lazy('donde vive'))
    foto = models.ImageField(upload_to=paciente_foto_path, verbose_name=_lazy('foto'), blank=True)
    firma = models.ImageField(upload_to=paciente_firma_path, verbose_name=_lazy('firma'), blank=True)

    # Datos responsable
    nombre_responsable = models.CharField(_lazy('nombre completo del responsable'), max_length=300)
    direccion_responsable = models.CharField(_lazy('dirección del responsable'), max_length=200)
    telefono_responsable = models.PositiveIntegerField(_lazy('telefono del responsable'), null=True, blank=True)

    # Menores de edad
    identificacion_padre = models.CharField(_lazy('identificación del padre'), max_length=15, blank=True)
    nombre_padre = models.CharField(_lazy('nombre completo del padre'), max_length=300, blank=True)
    identificacion_madre = models.CharField(_lazy('identificación de la madre'), max_length=15, blank=True)
    nombre_madre = models.CharField(_lazy('nombre completo de la madre'), max_length=300, blank=True)

    class Meta:
        verbose_name = _lazy('paciente')
        verbose_name_plural = _lazy('pacientes')

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)


class Orden(models.Model):
    """Modelo que maneja la información de una orden de un paciente."""

    COTIZANTE = 'C'
    BENEFICIARIO = 'B'
    SUBSIDIADO = 'A'
    PARTICULAR = 'P'
    VINCULADO = 'V'
    OTRO = 'O'
    AFILIACIONES = (
        (COTIZANTE, _lazy('Cotizante')),
        (BENEFICIARIO, _lazy('Beneficiario')),
        (SUBSIDIADO, _lazy('Subsidiado')),
        (PARTICULAR, _lazy('Particular')),
        (VINCULADO, _lazy('Vinculado')),
        (OTRO, _lazy('Otro'))
    )

    CONTRIBUTIVO = 'C'
    TIPOS_USUARIO = (
        (CONTRIBUTIVO, _lazy('Contributivo')),
        (SUBSIDIADO, _lazy('Subsidiado')),
        (VINCULADO, _lazy('Vinculado')),
        (PARTICULAR, _lazy('Particular')),
        (OTRO, _lazy('Otro'))
    )

    EFECTIVO = 'E'
    TARJETA = 'T'
    FORMAS_PAGO = (
        (EFECTIVO, _lazy('Efectivo')),
        (TARJETA, _lazy('Tarjeta'))
    )

    paciente = models.ForeignKey(Paciente, related_name='ordenes', verbose_name=_lazy('paciente'))
    fecha_orden = models.DateField(_lazy('Fecha de la orden'))
    autorizacion = models.CharField(_lazy('autorización'), max_length=50, blank=True)
    pendiente_autorizacion = models.BooleanField(_lazy('Pendiente por autorización'), default=False)
    afiliacion = models.CharField(_lazy('afiliación'), max_length=1, choices=AFILIACIONES)
    tipo_usuario = models.CharField(_lazy('tipo de usuario'), max_length=1, choices=TIPOS_USUARIO)
    anulada = models.BooleanField(_lazy('anulada'), default=False)
    razon_anulacion = models.CharField(_lazy('razón de anulación'), max_length=200, blank=True)
    forma_pago = models.CharField(_lazy('forma de pago'), max_length=2, choices=FORMAS_PAGO)
    empresa = models.ForeignKey('servicios.Plan', related_name='ordenes', verbose_name=_lazy('empresa'))
    institucion = models.ForeignKey('organizacional.Institucion', related_name='ordenes', verbose_name=_lazy('Institución'))
    servicios = models.ManyToManyField(
        'servicios.Servicio', through='ServicioOrden', related_name='ordenes', verbose_name=_lazy('servicios')
    )
    sucursal = models.ForeignKey('organizacional.Sucursal', related_name='ordenes', verbose_name=_lazy('sucursal'))

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'
    
    def __str__(self):
        return '{0} - {1}'.format(str(self.paciente), self.pk)


class ServicioOrden(models.Model):
    """Modelo para guardar los servicios que maneja una orden."""

    COOPAGO = 'CO'
    CUOTA_MODERADORA = 'CM'
    TIPOS_PAGO = (
        (COOPAGO, _lazy('Coopago')),
        (CUOTA_MODERADORA, _lazy('Cuota moderadora'))
    )

    orden = models.ForeignKey(Orden, related_name='servicios_orden', verbose_name=_lazy('orden'))
    servicio = models.ForeignKey('servicios.Servicio', related_name='servicios_orden', verbose_name=_lazy('servicio'))
    tipo_pago = models.CharField(_lazy('tipo de pago'), max_length=2, choices=TIPOS_PAGO)
    valor = models.PositiveIntegerField(_lazy('valor'))
    descuento = models.PositiveIntegerField(_lazy('descuento'))
    medico = models.ForeignKey('organizacional.Empleado', related_name='servicios', verbose_name=_lazy('medico'))

    class Meta:
        verbose_name = 'servicio orden'
        verbose_name_plural = 'servicios orden'
    
    def __str__(self):
        return '{} - {}'.format(self.orden.pk, self.servicio.nombre)


class Acompanante(ParentescoMixin, models.Model):
    """Modelo que guarda la información del acompañante de un paciente según el ordenamiento."""

    orden = models.OneToOneField(Orden, verbose_name=_lazy('orden'))
    asistio = models.BooleanField(_lazy('acompañante'))
    nombre = models.CharField(_lazy('nombre completo'), max_length=200)
    direccion = models.CharField(_lazy('dirección'), max_length=200)
    telefono = models.PositiveIntegerField(_lazy('teléfono'))

    class Meta:
        verbose_name = _lazy('acompañate')
        verbose_name_plural = _lazy('acompañates')
    
    def __str__(self):
        return self.nombre
