from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.db.models import Count
from django.db import IntegrityError
es_formats.DATETIME_FORMAT = "d M Y H:i:s"
from django.contrib import messages
from django.utils.translation import ngettext
from .forms import SubCategoryForm
from .models import *
class CategoryAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
            return Category.objects.annotate(subcategory_count=Count('categoria_id'))

    def subcategory_count(self, obj):
            return obj.subcategory_count
    subcategory_count.short_description = 'N° Subcategorias'
    subcategory_count.admin_order_field = 'subcategory_count'
    list_display = ('name',"subcategory_count" ,'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')
   
class SubCategoryAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
            return SubCategory.objects.annotate(product_count=Count('subcategoria_id'))

    def product_count(self, obj):
            return obj.product_count

    def save_model(self, request, obj, form, change):

        obj.user = request.user
        super().save_model(request, obj, form, change)

    product_count.short_description = 'N° Productos'
    product_count.admin_order_field = 'product_count'
  
    list_display = ('name','category','product_count', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')
class MarcasAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')
class ProductImageAdmin(admin.StackedInline):
    model=Productimage
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]
    list_display = ('name','subcategory','marca', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by','slug')


    
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Marcas,MarcasAdmin)
admin.site.register(Product,ProductAdmin)