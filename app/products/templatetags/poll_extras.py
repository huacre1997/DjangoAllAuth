from django import template
from django.conf import settings
from  products.models import Marcas,Category
register = template.Library()
@register.inclusion_tag('productList.html')
def show_results(poll):
    choices = poll.objects.all()
    return {'choices': choices}
     # marca=Marcas.objects.values("id","name","slug").annotate(brand_count=Count('marca_id'))
        # category=Category.objects.values("id","name","slug")
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def to_str(value):
    """converts int to string"""
    return str(value)
def type_of(value):
    """converts int to string"""
    return type(value)
def to_url(value):
    """converts int to string"""
    return '%s%s' % (settings.MEDIA_URL, value)
def priceSeparate(val,arg):
    if val!="":
        toArr=val.split(",")
        if arg==0:
            return toArr[0]
        else:
            return toArr[1]
    return ""


@register.filter
def get_item(dictionary, key):
  
    return dictionary[key].get("rate__count")
register.filter('url', to_url)
register.filter('priceSeparate', priceSeparate)

register.filter('to_str', to_str)
register.filter('type_of', type_of)