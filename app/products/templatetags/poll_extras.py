from django import template
from django.conf import settings
from  products.models import Marcas
register = template.Library()


def to_str(value):
    """converts int to string"""
    return str(value)
def type_of(value):
    """converts int to string"""
    return type(value)
def to_url(value):
    """converts int to string"""
    return '%s%s' % (settings.MEDIA_URL, value)
# def get_marca(value):
#     context=Marcas.objects.values("name").get(id=value)
#     return  context.get("name")
# register.filter('get_marca', get_marca)

register.filter('url', to_url)

register.filter('to_str', to_str)
register.filter('type_of', type_of)