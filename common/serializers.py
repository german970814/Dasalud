class PrefixFieldSerializerNameMixin(object):
    """Mixin que le agrega a todos campos de un serializer el nombre del serializer al que pertenece."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.style.update({'serializer': self.__class__.__name__})