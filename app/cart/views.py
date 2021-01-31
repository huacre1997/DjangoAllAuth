from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart as ObjCart
from products.models import Product
from django.apps import apps
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Cart, CartItem
from django.core import serializers
from django.views.decorators.cache import never_cache
import datetime

@never_cache
def CartView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user.id)
        data = CartItem.objects.values("product","product__image", "product__name",
                                    "product__marca__name", "product__price", "count").filter(cart=cart.id)
        context = {"object": data, "cartTotal": cart.total, "cartCount": cart.quantity}
        return render(request, "cartList.html", context)

    else:
        cartSession=ObjCart(request)
        context = {"object": cartSession.cart}
        return render(request, "cartList.html", context)
def cart_add(request):
    data = []
    post = json.loads(request.body.decode("utf-8"))

    model = apps.get_model('products', 'Product')
    if request.user.is_authenticated:
        # idp=Product.objects.get(slug=request.POST.get["id"])
        if request.method == "POST":

            cre = Cart.objects.get(user_id=request.user.id)

            if cre:

                p = CartItem.objects.filter(cart_id=cre.id)
                for i in p:
                    if i.product_id == post["id"]:
                        prod = p.get(product_id=post["id"])
                        cre.total=cre.total-(prod.product.price*prod.count)
                        cre.quantity=cre.quantity-prod.count
                        cre.save()
                        prod.count = i.count+int(post["quantity"])
                        prod.updated = datetime.datetime.now()
                        prod.save()
                        break

                else:
                    item = CartItem()
                    item.cart_id = cre.id
                    item.count = int(post["quantity"])
                    item.product_id = post["id"]
                    item.save()  
            else:
                print("else")

            return JsonResponse({"status":1,"quantity": cre.quantity}, safe=False)
    else:
        pro=Product.objects.get(id=post["id"])
        cart=ObjCart(request)
        cart.add(pro,int(post["quantity"]))
        cart.save()
        return JsonResponse({"status":0,"quantity":int(post["quantity"]),"total":cart.get_total_price()},safe=False)
    
def removeCart(request):
    if request.method == "POST":
        post = json.loads(request.body.decode("utf-8"))

        if request.user.is_authenticated:
            cre = Cart.objects.get(user_id=request.user.id)
            p = CartItem.objects.get(product_id=post["converted"],cart_id=cre.id)
            p.delete()           
            return JsonResponse({"count":p.count,"quantity":cre.quantity,"total":cre.total-(p.count*p.product.price)},safe=False)
        else:
            pro=Product.objects.get(id=post["converted"])

            cart = ObjCart(request)
            cart.update(pro,0)
            return JsonResponse({"status":0,"quantity":len(cart),"total":cart.get_total_price()}, safe=False)
def updateCart(request):
    if request.method == "POST":
        post = json.loads(request.body.decode("utf-8"))
        print(post)
        if request.user.is_authenticated:
            cre = Cart.objects.get(user_id=request.user.id)
            p = CartItem.objects.get(product_id=post["converted"],cart_id=cre.id)
            cre.total=cre.total-(p.product.price*p.count)
            cre.quantity=cre.quantity-p.count
            cre.save()
            p.count=int(post["newCount"])
            p.updated = datetime.datetime.now()
            p.save()
            return JsonResponse({"quantity":cre.quantity+int(post["newCount"]),"total":cre.total+(p.count*p.product.price)},safe=False)
        else:
            pro=Product.objects.get(id=post["converted"])
            cartSession=ObjCart(request)
            cartSession.update(pro,int(post["newCount"]))

            return JsonResponse({"quantity":len(cartSession),"total":cartSession.get_total_price()},safe=False)
