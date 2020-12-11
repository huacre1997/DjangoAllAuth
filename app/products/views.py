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
        chesubcat=request.GET.get("sc")
        if chesubcat==None and order==None and brand==None:
            response=Product.objects.values("id","name","price","marca__name","image").distinct()

        if chesubcat and order and brand==None:
            print("chekcsubcat and order and brand none")
            if order=="priceLower":
                response=Product.objects.get_category_product(chesubcat).order_by("price")
            elif order=="priceHigher":
                print("else")
                response=Product.objects.get_category_product(chesubcat).order_by("price").reverse()           

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
            response=Product.objects.get_category_product(chesubcat)
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
    post = Paginator(response,4)
    if(request.GET.get("page")):
        page_obj = post.page(request.GET.get("page"))  
    else:
        page_obj = post.page(1)
            
    context={"product":page_obj,"text":'Nuestros productos.',"tag":"Productos","productActive":"active"}
    return render(request,"productList.html",context)


def byCategory(request,slug):
    if request.method=="GET":
        data = []
        brand=request.GET.get("brand")
        order=request.GET.get("order")
        
        node = Category.objects.get(slug=slug)

        if node.is_child_node():
            category=Product.objects.values("id","name","price","marca__name","image").filter(category=node)
        else:
            category=Product.objects.values("id","name","price","marca__name","image").filter(category__parent=node.get_root().id)
        if order=="priceLower" and brand:
            print("priceLower and brand")
            context=category.filter(marca__name=brand).order_by("price")
        elif order=="priceHigher" and brand:
            print("priceHigher and brand")
            context=category.filter(marca__name=brand).order_by("price").reverse()
        elif brand:
            print("brand")

            context=category.filter(marca__name=brand)
        elif order:
            print("order")

            if  order=="priceLower":
                context=category.order_by("price")
            else:
                context=category.order_by("price").reverse()
        context=category
        post = Paginator(context,1)
        if(request.GET.get("page")):
            page_obj = post.page(request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return render(request,"productList.html",{"product":page_obj ,"tag":"Productos","tag2":node,"displayCat":"none"})
class byMarcas(TemplateView):
    template_name="productList.html"
    def get(self,request,*args, **kwargs):
        data = []
        subcat=request.GET.get("sc")
        marca = kwargs['marca']
        order=request.GET.get("order")

        if subcat==None or subcat=="":
            subcat=subcat
        else:
            subcat=subcat.split(",")
        marcas=Product.objects.values("id","name","price","marca__name","image").filter(marca__slug=marca)
        print("Order es "+str(order))
        print("categ es "+str(subcat))
        if subcat:
            print("subcat")

            context=marcas.filter(category__id__in=subcat)
      
        elif order=="priceLower" and subcat:
            print("priceLower and subcat")
            context=marcas.filter(category__id__in=subcat).order_by("price")
        elif order=="priceHigher" and subcat:
            print("priceHigher and subcat")
            context=marcas.filter(category__id__in=subcat).order_by("price").reverse()
        elif order=="priceLower" and subcat==None:
            print("priceLower")
            context=marcas.order_by("price")
        elif order=="priceHigher"  and subcat==None:
            print("proceHighuer")
            context=marcas.orderHigher().order_by("price").reverse()
        context=marcas
        post = Paginator(context,1)
        if(request.GET.get("page")):
            page_obj = post.page(request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return render(request,self.template_name,{"product":page_obj ,"tag":"Productos","tag2":marca,"productActive":"active","displayBrand":"none"})


def getProduct(request,id):
    if request.method == 'GET':
        item=Product.objects.get(id=id)
        print(item.price)
        data = {
                'response': render_to_string("modal.html", {'product': item}, request=request)}
        return JsonResponse(data,safe=False)
class Search(TemplateView):
    template_name="productList.html"

    def get(self,request,*args, **kwargs):
        search=request.GET.get("q")
        brand=request.GET.get("brand")
        categ=request.GET.get("sc")
        order=request.GET.get("order")
        print("Order es "+str(order))

        print("brand es "+str(brand))    
        print("categ es "+str(categ))
        print("search es "+str(search))
        
        if categ==None or categ=="":
            categ=categ
        else:
            categ=categ.split(",")

        searchby=Product.objects.values("id","name","price","marca__name","image")
        if order==None and brand==None and (categ==None or categ=="") and search=="":
            context=searchby
        elif order==None and search=="" and brand and categ :
            context=searchby.filter(marca__name=brand,category__in=categ)
        elif order==None and search=="" and  brand==None and categ:    
            context=searchby.filter(category__in=categ)
        elif order==None and search=="" and brand and categ==None :
            context=searchby.filter(marca__name=brand)
        elif order==None and search and brand==None and categ :
            context=searchby.filter(name__icontains=search,category__in=categ)      
        elif order==None and search and brand==None and (categ==None or categ=="") :
            context=searchby.filter(name__icontains=search)       
        # elif order==None and search and categ=="" and  brand==None:    
        #     context=searchby.filter(name__icontains=search)
        elif order==None and search and (categ=="" or categ==None)  and brand :
            context=searchby.filter(marca__name=brand,name__icontains=search)
        # elif order==None and search and brand and categ==None :
        #     context=searchby.filter(marca__name=brand,name__icontains=search) 
      
        elif  order and search=="" and categ   and brand:
            if order=="priceLower":
                context=searchby.filter(category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(category__in=categ,marca__name=brand).order_by("price").reverse() 
        elif  order and search and (categ=="" or categ==None)  and brand:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price").reverse()  
        # elif order and search and brand and categ==None :
        #     if order=="priceLower":
        #         context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price")
        #     elif order=="priceHigher":
        #         context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price").reverse()      
        elif  order and search and (categ=="" or categ==None)  and brand==None:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search).order_by("price").reverse()       
        # elif order and search and categ==None and brand==None:    
        #     if order=="priceLower":
        #         context=searchby.filter(name__icontains=search).order_by("price")
        #     elif order=="priceHigher":
        #         context=searchby.filter(name__icontains=search).order_by("price").reverse()      
              
        elif  order and search and categ and brand:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,category__in=categ,marca__name=brand).order_by("price").reverse()   
        elif  order and search=="" and categ==None and brand:
            if order=="priceLower":
                context=searchby.filter(marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(marca__name=brand).order_by("price").reverse()           
        elif  order and search and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,category__in=categ).order_by("price").reverse() 
        elif  order and search=="" and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(category__in=categ).order_by("price").reverse()           
        elif  order and search=="" and brand==None and categ =="" :
            if order=="priceLower":
                context=searchby.order_by("price")
            elif order=="priceHigher":
                context=searchby.order_by("price").reverse()   
        elif  order and search=="" and categ==None  and brand==None:
            if order=="priceLower":
                context=searchby.order_by("price")
            elif order=="priceHigher":
                context=searchby.order_by("price").reverse()   
        post = Paginator(context,3)
        if(request.GET.get("page")):
            page_obj = post.page(request.GET.get("page"))  
        else:
            page_obj = post.page(1)
                
        context={"product":page_obj,"tag3":search,"tag":"Productos"}
        return render(request,"productList.html",context)
