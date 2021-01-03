from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST 
from .cart import Cart 
from django.apps import apps
from django.views.generic import TemplateView

class CartView(TemplateView):
    template_name = "cartList.html"

def cart_add(request, id):  
    model = apps.get_model('products', 'Product')

    if request.method=="POST": 
        data=[]
        cart = Cart(request)    
        product = get_object_or_404(model, id=id) 
        cart.add(product=product,quantity=1,override_quantity=False) 
        context={"total":cart.get_total_price(),
        "cantidad":cart.__len__(),
        "data":cart.__dict__["cart"]}
        return JsonResponse(context,safe=False) 
def removeCart(request):  
    if request.method=="POST": 

        cart = Cart(request)    
        cart.clear()
        print(cart.__dict__)
        return JsonResponse(cart.__dict__["cart"],safe=False) 