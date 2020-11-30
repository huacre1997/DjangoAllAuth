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
from django.core.paginator import (
    InvalidPage, PageNotAnInteger, EmptyPage, Paginator)
from django.template.loader import render_to_string
from fast_pagination.helpers import FastPaginator
from django.views.decorators.cache import cache_page

# def ProductList(request):
#     model=Product
#     template_name="productList.html"
#     context_object_name = "product"
#     paginate_by=3
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
 
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["marca"]=Marcas.objects.values("id","name","slug").annotate(brand_count=Count('marca_id'))
#         context["category"]=Category.objects.values("id","name","slug")
#         context["subcategory"]=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   

#         return context


# @cache_page(60 * 15)
def ProductList(request):
    
    if request.method == 'GET':
        brand=request.GET.get("brand")
        order=request.GET.get("order")
        chesubcat=request.GET.get("subcategory")
        if chesubcat==None and order==None and brand==None:
            response=Product.objects.values("id","name","price","marca__name","image").distinct()

        if chesubcat and order and brand==None:
            print("chekcsubcat and order and brand none")
            if order=="priceLower":
                response=Product.objects.get_subcategory_product(chesubcat).order_by("price")
            elif order=="priceHigher":
                print("else")
                response=Product.objects.get_subcategory_product(chesubcat).order_by("price").reverse()           

        elif chesubcat and brand and order:
            print("checksubcat and brand and order")
            if order=="priceLower":
                response=Product.objects.filterMultiple(chesubcat,brand).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.filterMultiple(chesubcat,brand).order_by("price").reverse()
            response=Product.objects.filterMultiple(chesubcat,brand) 
        
        elif chesubcat and brand:
            print("checksubcat and brand ")
            response=Product.objects.filterMultiple(chesubcat,brand)             
        elif order=="priceLower" and brand:
            print("priceLower and brand")
            response=Product.objects.get_brands_product(brand).order_by("price")
            
        elif order=="priceHigher" and brand:
            print("pricehiguer and brand")
            response=Product.objects.get_brands_product(brand).order_by("price").reverse()
        elif chesubcat:
            print("checksubcat")
            response=Product.objects.get_subcategory_product(chesubcat)
        elif brand:
            print("brand")
            response = Product.objects.get_brands_product(brand)
        elif order=="priceLower":
            response=Product.objects.orderLower()
        elif order=="priceHigher":
            response=Product.objects.orderHigher()

        # marca=Marcas.objects.values("id","name","slug").annotate(brand_count=Count('marca_id'))
        # category=Category.objects.values("id","name","slug")
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
        # product=Product.objects.select_related("marca").values("id","name","price","image")
    
       
        # page_obj = paginator2.get_page(page_number)
    else:
        print("else")
    post = Paginator(response,3)
    if(request.GET.get("page")):
        page_obj = post.page(request.GET.get("page"))  
    else:
        page_obj = post.page(1)
            
    context={"product":page_obj}
    return render(request,"productList.html",context)
def filter(request):
    if request.method == 'GET':
        data={}
        brand=request.GET.get("brand")  
        order=request.GET.get("order")
        chesubcat=request.GET.get("subcategory")
       
        response=Product.objects.values("id","slug","name","marca__name","price","image")
        if chesubcat and order and brand==None:
            print("chekcsubcat and order and brand none")
            if order=="priceLower":
                response=Product.objects.get_subcategory_product(chesubcat).order_by("price")
            elif order=="priceHigher":
                print("else")
                response=Product.objects.get_subcategory_product(chesubcat).order_by("price").reverse()           

        elif chesubcat and brand and order:
            print("checksubcat and brand and order")
            if order=="priceLower":
                response=Product.objects.filterMultiple(chesubcat,brand).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.filterMultiple(chesubcat,brand).order_by("price").reverse()
            response=Product.objects.filterMultiple(chesubcat,brand) 
        
        elif chesubcat and brand:
            print("checksubcat and brand ")
            response=Product.objects.filterMultiple(chesubcat,brand)             
        elif order=="priceLower" and brand:
            print("priceLower and brand")
            response=Product.objects.get_brands_product(brand).order_by("price")
            
        elif order=="priceHigher" and brand:
            print("pricehiguer and brand")
            response=Product.objects.get_brands_product(brand).order_by("price").reverse()
        elif chesubcat:
            print("checksubcat")
            response=Product.objects.get_subcategory_product(chesubcat)
        elif brand:
            print("brand")
            response = Product.objects.get_brands_product(brand)
        elif order=="priceLower":
            response=Product.objects.orderLower()
        elif order=="priceHigher":
            response=Product.objects.orderHigher()
        # objects = list(response[:3 * 3]) #2 !!!
        # paginator = Paginator(objects, 3)
        # post = paginator.page(request.GET.get("page"))        # page=request.GET.get("page")
        # posts=paginator.page(page)
        # context={"product":queryset,"marca":marca,"category":categ,"subcategory":subcategory}
        # return render(request,"productList.html",context)
        
        data = {
                'response': render_to_string("productList.html", {'product ': response}, request=request)}
        return JsonResponse(data)
        # try:
        #     data=[]
        #     for i in queryset:
        #         data.append(i.toJSON())
        #     return JsonResponse(data,safe=False)
        # except Exception as e:
        #     print(e)
class getCat(TemplateView):
    template_name="index.html"
    def get(self,request,*args, **kwargs):
        data = []
        cat = kwargs['cat']
        for i in Category.objects.values("id","name","slug").filter(slug=cat):
            data.append(i.toJSON())
 
        return JsonResponse(data,safe=False)

def getProduct(request,id):

    if request.method == 'GET':
        item=Product.objects.get(id=id)
        print(item.price)
        data = {
                'response': render_to_string("modal.html", {'product': item}, request=request)}
        return JsonResponse(data,safe=False)
def search(request):
    search=request.GET.get("q")
    brand=request.GET.get("brand")
    print(brand)
    if brand and search:
        print("brand and search")
        context=Product.objects.values("id","name","price","marca__name","image").filter(name__icontains=search).filter(marca__name=brand)
    if search and brand==None:    
        print(" search")

        context=Product.objects.filter(name__icontains=search)
    post = Paginator(context,3)
    if(request.GET.get("page")):
        page_obj = post.page(request.GET.get("page"))  
    else:
        page_obj = post.page(1)
            
    context={"product":page_obj,"item":search}
    return render(request,"productList.html",context)
