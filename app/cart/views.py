from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST 
from .cart import Cart 
from products.models import Product
from django.apps import apps
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Cart
from django.core import serializers
from django.views.decorators.cache import never_cache
@never_cache
def CartView(request):
    
    data=Cart.objects.prefetch_related("product").filter(user_id=request.user)
    context={"object":data}    

    return render(request,"cartList.html",context)
# class CartView(TemplateView):
#     template_name = "cartList.html"
#     model=Cart
#     def get(self,request,*args, **kwargs):
#         if self.request.GET:
#             print("hola")
#         else:
#             print("else")

#         data=Cart.objects.select_related("product").filter(user_id=request.user)
#         context={"object":data}    

#         return render(request,self.template_name,context)

#     def post(self, *args,**kwargs):
#         print("entro a post")
        # return HttpResponse("aea")W
    # def post(self,*args,**kwargs):
    #     context=Cart.objects.select_related("product").filter(user_id=self.request.user)
    #     data = []

    #     for book in context:
    #         data.append({'marca': book.product.marca.name,
    #          'name': book.product.name, 
    #          'price': book.product.price,
    #         'image': book.product.image.url,
    #         "quantity":book.quantity,
    #         "created":book.created,
    #         "updated":book.updated,

    #          })

        # response = serializers.serialize("json", data)
        # return JsonResponse(data, safe=False)
def cart_add(request):  
    model = apps.get_model('products', 'Product')
    if request.user.is_authenticated:
        # idp=Product.objects.get(slug=request.POST.get["id"])
        if request.method=="POST": 
            post = json.loads(request.body.decode("utf-8"))

            data= Cart()
            data.user=request.user
            data.quantity=post["quantity"]
            data.product_id=post["id"]
            data.save()
            amount=Cart.objects.amount(request.user)
            return JsonResponse({"quantity":amount},safe=False) 

    else:
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
    if request.user.is_authenticated():
        print("is")
    if request.method=="POST": 

        cart = Cart(request)    
        cart.clear()
        print(cart.__dict__)
        return JsonResponse(cart.__dict__["cart"],safe=False) 