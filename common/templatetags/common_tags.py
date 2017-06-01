from django import template
from rest_framework.renderers import JSONRenderer

register = template.Library()

@register.filter
def to_json(campo):
    """
    :returns:
        Un json con las opciones del campo dentro de un array.
    
    :param campo:
        El campo al cual se le van a serializar las opciones.
    """

    json = []
    for option in campo.iter_options():
        json.append({'value': option.value, 'label': option.display_text})
    
    return JSONRenderer().render(json)
