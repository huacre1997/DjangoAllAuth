from decimal import Decimal
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST 
from django.apps import apps
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.base import TemplateView
from requests import models
from accounts.models import *
from cart.models import Cart
from django.views.decorators.cache import never_cache
from .models import Order
from .pay import *
class CheckOutView(TemplateView,LoginRequiredMixin):
    template_name = "checkout.html"

    redirect_field_name = 'index'

    def post(self, *args,**kwargs):
        cart=Cart.objects.get(user=self.request.user.id)
        data=json.loads(self.request.body.decode("utf-8"))
        order_id=data["orderID"]
        detalle=GetOrder().get_order(order_id)
        detalle_precio=Decimal(detalle.result.purchase_units[0].amount.value)
        print(data["address"])
        if detalle_precio==cart.total:
            trx=CaptureOrder().capture_order(order_id,debug=True)
            ord=Order()
            ord.order_id=trx.result.id
            ord.client_id=self.request.user.id
            ord.cart=cart
            ord.address_id=data["address"]
            ord.total=detalle_precio
            ord.save()
            print("EXITO")
            return JsonResponse({"response":"ok"},safe=False)


    def get_context_data(self, **kwargs):

        context = super(CheckOutView, self).get_context_data(**kwargs)
        # cart = Cart.objects.get(user=self.request.user.id)

        context["address"]=Adress.objects.filter(user_id=self.request.user.id)
        # context["cartTotal"]=cart.total
        # context["cartCount"]=cart.quantity

        return context

# 1. Import the PayPal SDK client created in `Set up Server-Side SDK` section.
from .pay import PayPalClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest


class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
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


