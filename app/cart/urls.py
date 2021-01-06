from django.urls import path, include
from django.conf import settings
from .views import *


urlpatterns = [
    path('carrito/add/', cart_add, name="add_cart"),

    path('carrito/', CartView, name="cart"),
    path('carrito/remove', removeCart, name="clean_cart"),

] 
