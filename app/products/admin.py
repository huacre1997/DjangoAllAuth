from django.contrib import admin

from .models import *
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by','created','modified_by','modified',"status")

    exclude = ('created_by','modified_by')

admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)