from django.contrib import admin
from .models import Order
class OrdersAdmin(admin.ModelAdmin):
    pass



admin.site.register(Order,OrdersAdmin)