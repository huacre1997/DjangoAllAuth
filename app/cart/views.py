from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST 
from .cart import Cart 
from django.apps import apps
def cart_add(request, id):  
    if request.method=="POST": 
        data=[]
        model = apps.get_model('products', 'Product')
    
        cart = Cart(request)    
        product = get_object_or_404(model, id=id) 
        cart.add(product=product,quantity=1,override_quantity=False) 
        return JsonResponse(json.dumps(cart.__dict__),safe=False) 
