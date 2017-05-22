from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


class Paciente(models.Model):
    """Modelo para guardar la información de un paciente."""

    FEMENINO = 'F'
    MASCULINO = 'M'
    GENEROS = (
        (FEMENINO, _lazy('Femenino')),
        (MASCULINO, _lazy('Masculino')),
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
        (NUMERO_UNICO_ID, 'Número único de identificación'),
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
        (UNION_LIBRE, _lazy('Unión libre')),
    )

    RURAL = 'R'
    URBANO = 'U'
    ZONAS = (
        (URBANO, _lazy('Urbano')),
        (RURAL, _lazy('Rural')),
    )

    AB = 'AB'
    O_POSITIVO = 'O+'
    O_NEGATIVO = 'O-'
    GRUPOS_SANGUINEOS = (
        (O_NEGATIVO, 'O+'),
        (O_POSITIVO, 'O-'),
        (AB, 'AB'),
    )

    OTRO = 'O'
    NEGRO = 'N'
    INDIGENA = 'I'
    DESPLAZADO = 'D'
    GRUPOS_ETNICOS = (
        (DESPLAZADO, _lazy('Desplazado')),
        (INDIGENA, _lazy('Indigena')),
        (NEGRO, _lazy('Negro')),
        (OTRO, _lazy('Otro')),
    )

    nombres = models.CharField(_lazy('nombres'), max_length=150)
    apellidos = models.CharField(_lazy('apellidos'), max_length=150)
    genero = models.CharField(_lazy('género'), max_length=1, choices=GENEROS)
    fecha_nacimiento = models.DateField(_lazy('fecha de nacimiento'))
    fecha_ingreso = models.DateField(_lazy('fecha de ingreso'))
    tipo_documento = models.CharField(_lazy('tipo de documento'), max_length=2, choices=TIPO_DOCUMENTOS)
    numero_documento = models.IntegerField(_lazy('número de documento'))
    estado_civil = models.CharField(_lazy('estado civil'), max_length=2, choices=ESTADOS_CIVILES)
    zona = models.CharField(_lazy('zona'), max_length=1, choices=ZONAS)
    direccion = models.CharField(_lazy('dirección'), max_length=200)
    telefono = models.IntegerField(_lazy('telefono'), null=True, blank=True)
    celular = models.IntegerField(_lazy('celular'), null=True, blank=True)
    email = models.EmailField(_lazy('email'))
    grupo_sanguineo = models.CharField(_lazy('grupo sanguineo'), max_length=2, choices=GRUPOS_SANGUINEOS, blank=True)
    grupo_etnico = models.CharField(_lazy('grupo etnico'), max_length=1, choices=GRUPOS_ETNICOS, blank=True)
    activo = models.BooleanField(_lazy('activo'), default=True)

    # profesion = models.ForeignKey('profesion', related_name='pacientes', verbose_name=_lazy('profesión'),  null=True, blank=True)
    # lugar_nacimiento = models.ForeignKey('lugar de nacinon', related_name='pacientes', verbose_name=_lazy('nacio en'))

    class Meta:
        verbose_name = _lazy('paciente')
        verbose_name_plural = _lazy('pacientes')

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)