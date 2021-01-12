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
from accounts.models import District,Province,Adress

class CheckOutView(TemplateView):
    
    template_name = "checkout.html"
    
    def get_context_data(self, **kwargs):

        context = super(CheckOutView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=request.user.id)

        context["address"]=Adress.objects.filter(user_id=self.request.user.id)
        context["cartTotal"]=cart.total
        context["cartCount"]=cart.quantity

        return context