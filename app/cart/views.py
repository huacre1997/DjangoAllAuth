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


@never_cache
def CartView(request):

    cart = Cart.objects.get(user=request.user.id)
    data = CartItem.objects.values("product__image", "product__name",
                                   "product__marca__name", "product__price", "count").filter(cart=cart.id)
    context = {"object": data, "cartTotal": cart.total}

    return render(request, "cartList.html", context)
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
    data = []
    post = json.loads(request.body.decode("utf-8"))
    print(post)
    import datetime

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
                        prod.count = i.count+int(post["quantity"])
                        prod.updated = datetime.datetime.now()
                        prod.save()
                        break

                else:
                    print("forlse")
                    item = CartItem()
                    item.cart_id = cre.id
                    item.count = int(post["quantity"])
                    item.product_id = post["id"]
                    item.save()  
            else:
                print("else")

            return JsonResponse({"quantity": cre.quantity}, safe=False)

    # else:
    #     post = json.loads(request.body.decode("utf-8"))
    #     if request.method=="POST":
    #         data=[]
    #         cart = Cart(request)
    #         product = get_object_or_404(model, id=id)
    #         cart.add(product=product,quantity=1,override_quantity=False)
    #         context={"total":cart.get_total_price(),
    #         "cantidad":cart.__len__(),
    #         "data":cart.__dict__["cart"]}
    #         print(cart.__dict__["cart"])
    #         return JsonResponse(context,safe=False)


def removeCart(request):
    if request.user.is_authenticated():
        print("is")
    if request.method == "POST":

        cart = Cart(request)
        cart.clear()
        print(cart.__dict__)
        return JsonResponse(cart.__dict__["cart"], safe=False)
