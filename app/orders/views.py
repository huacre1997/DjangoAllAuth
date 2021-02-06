import decimal
from culqi.resources import Charge
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from .pay import PayPalClient
from culqi.client import Culqi
from decimal import Decimal
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import render

from django.apps import apps
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.base import TemplateView, View
from paypalhttp.serializers.json_serializer import Json
from requests import models
from accounts.models import *
from cart.models import Cart,CartItem
from django.views.decorators.cache import never_cache
from .models import Order,OrderDetails
from .pay import *


class CheckOutView(TemplateView):
    template_name = "checkout.html"
    # login_url = '/login'

    @never_cache
    def dispatch(self, request, *args, **kwargs):

        return super(CheckOutView, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user.id)
        data = json.loads(self.request.body.decode("utf-8"))
        order_id = data["orderID"]
        detalle = GetOrder().get_order(order_id)
        detalle_precio = Decimal(detalle.result.purchase_units[0].amount.value)
        if detalle_precio == cart.total:
            trx = CaptureOrder().capture_order(order_id, debug=True)
            ord = Order()
            ord.order_id = trx.result.id
            ord.client_id = self.request.user.id
            ord.cart = cart
            ord.address_id = data["address"]
            ord.total = detalle_precio
            ord.save()
            print("EXITO")
            return JsonResponse({"response": "ok"}, safe=False)

    def get_context_data(self, **kwargs):

        context = super(CheckOutView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user.id)

        context["address"] = Adress.objects.filter(
            user_id=self.request.user.id)
        context["cartTotal"] = cart.total
        context["cartCount"] = cart.quantity
        if self.request.user.is_authenticated:
            context["auth"] = 1
        return context


def charges(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user.id)
        token = request.POST['token']
        email = request.POST['email']
        address= request.POST["address"]
        count = int(request.POST['count'])
        get=request.POST["amount"]
        print(get)
      
        
        if cart.total == Decimal(get)/100:
            dir_charge = {
                "amount":int(get),
                "capture": False,
                "currency_code": "PEN",
                "description": "Venta",
                "email": email,
                "installments": 0,
                "source_id": token,
            }
            culqi = Culqi(public_key="pk_test_3dbf717e5fbefb71",
                      private_key="sk_test_86ea6b22eb0c1319")
            charge = culqi.charge.create(dir_charge)
            if charge["data"]["object"]!='error'
                ord = Order()
            
                ord.client_id = request.user.id
                ord.cart = cart
                ord.address_id =address
                ord.total = cart.total
                print("EXITO")
                ord.save()

                items= CartItem.objects.filter(cart_id=cart.id)

                for i in items:
                    data=OrderDetails()
                    data.product=i.product
                    data.count=i.count
                    data.order=ord
                    data.save()
                items.delete()
                cart.quantity=0
                cart.total=0
                cart.save()
            
                return JsonResponse(charge, safe=False)
        else:
            JsonResponse("Error descontrolado..")
    return JsonResponse("only POST method", safe=False)

# 1. Import the PayPal SDK client created in `Set up Server-Side SDK` section.


class CaptureOrder(PayPalClient):

    # 2. Set up your server to receive a call from the client
    """this sample function performs payment capture on the order.
    Approved order ID should be passed as an argument to this function"""

    def capture_order(self, order_id, debug=False):
        """Method to capture order using order_id"""
        request = OrdersCaptureRequest(order_id)
        # 3. Call PayPal to capture an order
        response = self.client.execute(request)
        # 4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
        # if debug:
        #     print( 'Status Code: ', response.status_code)
        #     print ('Status: ', response.result.status)
        #     print ('Order ID: ', response.result.id)
        #     print ('Links: ')
        #     for link in response.result.links:
        #         print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        #     print( 'Capture Ids: ')
        #     for purchase_unit in response.result.purchase_units:
        #         for capture in purchase_unit.payments.captures:
        #             print( '\t', capture.id)
        #     print ("Buyer:")
        #     print("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
        #         response.result.payer.name.given_name + " " + response.result.payer.name.surname,
        #         response.result.payer.phone.phone_number.national_number))
        return response
