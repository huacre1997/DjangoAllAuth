from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST 
from .cart import Cart 
from django.apps import apps
@require_POST 
def cart_add(request, product_id):   
    model = apps.get_model('products', 'Product')
 
    cart = Cart(request)    
    product = get_object_or_404(model, id=product_id)    
    cart.add(product=product,quantity=1,override_quantity=False  ) 
    print(cart)
    return redirect('products:getProducList') 
