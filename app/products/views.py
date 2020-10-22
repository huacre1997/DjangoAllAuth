from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
class CategoryView(TemplateView):
        model=Category
        template_name="index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Category"] = Category.objects.all()
        return context
    
