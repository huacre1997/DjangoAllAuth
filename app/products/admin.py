from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.db.models import Count
from django.db import IntegrityError
es_formats.DATETIME_FORMAT = "d M Y H:i:s"
from django.contrib import messages
from django.utils.translation import ngettext
from .models import *
from mptt.admin import DraggableMPTTAdmin
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50

    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    exclude = ('created_by','modified_by','slug')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
   

class MarcasAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')
class ProductImageAdmin(admin.StackedInline):
    model=Productimage
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]
    list_display = ('name','category','marca', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')




admin.site.register(Category,CategoryAdmin)
admin.site.register(Marcas,MarcasAdmin)
admin.site.register(Product,ProductAdmin)