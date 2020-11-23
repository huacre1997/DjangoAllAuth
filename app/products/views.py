from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from .models import *
from django.http import JsonResponse
from  base.mixins import CustomMixin
from django.shortcuts import redirect,HttpResponse
from django.views import View
from django.db.models import Q
import json
from django.core import serializers
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator


class ProductList(ListView):
    model=Product
    template_name="productList.html"
    context_object_name = "product"
    paginate_by=6
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["marca"]=Marcas.objects.all()
        return context
        
# def filter():
#         def post(self,request,*args, **kwargs):
#         data={}

#         categ=Category.objects.values("id","name","slug")
#         subcategory= SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))     
#         marca=Marcas.objects.all()
#         brand=self.request.GET.get("brand")
#         order=self.request.GET.get("order")
#         chesubcat=self.request.GET.get("subcategory")
       
#         queryset=Product.objects.values("id","slug","name","marca__name","price","image")
#         if chesubcat and order and brand==None:
#             print("chekcsubcat and order and brand none")
#             if order=="priceLower":
#                 queryset=Product.objects.get_subcategory_product(chesubcat).order_by("price")
#             elif order=="priceHigher":
#                 print("else")
#                 queryset=Product.objects.get_subcategory_product(chesubcat).order_by("price").reverse()           

#         elif chesubcat and brand and order:
#             print("checksubcat and brand and order")
#             if order=="priceLower":
#                 queryset=Product.objects.filterMultiple(chesubcat,brand).order_by("price")
#             elif order=="priceHigher":
#                 queryset=Product.objects.filterMultiple(chesubcat,brand).order_by("price").reverse()
#             queryset=Product.objects.filterMultiple(chesubcat,brand) 
        
#         elif chesubcat and brand:
#             print("checksubcat and brand ")
#             queryset=Product.objects.filterMultiple(chesubcat,brand)             
#         elif order=="priceLower" and brand:
#             print("priceLower and brand")
#             queryset=Product.objects.get_brands_product(brand).order_by("price")
            
#         elif order=="priceHigher" and brand:
#             print("pricehiguer and brand")
#             queryset=Product.objects.get_brands_product(brand).order_by("price").reverse()
#         elif chesubcat:
#             print("checksubcat")
#             queryset=Product.objects.get_subcategory_product(chesubcat)
#         elif brand:
#             print("brand")
#             queryset = Product.objects.get_brands_product(brand)
#         elif order=="priceLower":
#             queryset=Product.objects.orderLower()
#         elif order=="priceHigher":
#             queryset=Product.objects.orderHigher()
#         # paginator=Paginator(queryset,3)
#         # page=request.GET.get("page")
#         # posts=paginator.get_page(page)
#         # context={"product":queryset,"marca":marca,"category":categ,"subcategory":subcategory}
#         # return render(request,"productList.html",context)
#         try:
#             data=[]
#             for i in queryset:
#                 data.append(i.toJSON())
#             return JsonResponse(data,safe=False)
#         except Exception as e:
#             print(e)
class getCat(TemplateView):
    template_name="index.html"
    def get(self,request,*args, **kwargs):
        data = []
        cat = kwargs['cat']
        for i in SubCategory.objects.values("id","name","slug").filter(category__slug=cat):
            data.append(i.toJSON())
 
        return JsonResponse(data,safe=False)

class getProduct(DetailView):

    model=Product  
    template_name="modal.html"
    context_object_name = 'obj'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self,response,*args, **kwargs):
        data=[]
        try:
            for i in Product.objects.filter(slug=self.get_object().slug):
                item=i.toJSON()
                data.append(item)

        except:
            pass
        return JsonResponse(data,safe=False)