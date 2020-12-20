from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from .models import *
from django.http import JsonResponse
from django.shortcuts import redirect,HttpResponse,HttpResponseRedirect
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
from django.views.decorators.cache import cache_page
from .forms import RatingForm
from django.db.models import Q, Count,Avg
from django.db import connection
class ProductDetailView(DetailView):
    model=Product
    template_name="product_detail.html"
    form_class=RatingForm
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        qs=Product.objects.defer("meta_description","meta_keywords","created","modified","created_by_id","modified_by_id","status")
        return qs
    def post(self, request, *args, **kwargs):
        form=RatingForm(request.POST)    
        self.object = self.get_object()
        if form.is_valid():
            
            data=Comment()
            data.author=form.cleaned_data["author"]
            data.comment=form.cleaned_data["comment"]       
            data.ip=request.META.get("REMOTE_ADDR")
            data.rate=form.cleaned_data["rate"]
            data.product_id=self.object.id
            data.save()
            with connection.cursor() as cursor:
                cursor.execute("select * from avgRating("+str(self.object.id)+")")
                row = cursor.fetchone() 
            self.object.updateRate(row[0])
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)   
        else:
            return HttpResponse(form.errors)
    def get_context_data(self, **kwargs):
        data=[]
        total=0
        context = super().get_context_data(**kwargs)
        context["image"] = Productimage.objects.filter(product=self.object.id)
        q=Comment.objects.values("rate").filter(product=self.object.id).order_by("rate").reverse().annotate(Count('rate'))
        with connection.cursor() as cursor:
            cursor.execute("select * from getRating("+str(self.object.id)+")")
            row = cursor.fetchall()       
        for i in row:
            data.append(i[1])
               
        for k,i in enumerate(data):
            total+=i*(k+1)
        from functools import reduce
        staravg=0
        suma=reduce((lambda a,b: a+b),data) 
        if suma!=0:
            staravg=round(total/suma,1)
        context["starsAvg"]=staravg
        context["starsCount"]=data[::-1]
        post = Paginator(Comment.objects.filter(product_id=self.object.id).order_by("created_date").reverse(),4)
        if  self.request.GET.get('page'):
            page_obj = post.page( self.request.GET.get('page'))  
        else:
            page_obj = post.page(1)
        context["comment"]=page_obj
        return context


@cache_page(60 * 15)
def ProductList(request):
    
    if request.method == 'GET':
        brand=request.GET.get("brand")
        order=request.GET.get("order")
        chesubcat=request.GET.get("sc")
        price=request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")

        if price and chesubcat==None and order==None and brand==None:
            response=Product.objects.get_price_product(price)
        elif price and chesubcat and order==None and brand:
            response=Product.objects.filterMultiple(chesubcat,brand,price)
        elif price and chesubcat and order==None and brand==None:
            response=Product.objects.catxprice(price,chesubcat)
        elif price and chesubcat and order and brand==None:
            if order=="priceLower":
                response=Product.objects.catxprice(price,chesubcat).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.catxprice(price,chesubcat).order_by("price").reverse()    
        elif price and chesubcat and order and brand:
            if order=="priceLower":
                response=Product.objects.filterMultiple(chesubcat,brand,price).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.filterMultiple(chesubcat,brand,price).order_by("price").reverse()
        elif price and chesubcat==None and order==None and brand:
            response=Product.objects.brandxprice(brand,price)
        elif price and chesubcat==None and order and brand==None:
            if order=="priceLower":
                response=Product.objects.get_price_product(price).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.get_price_product(price).order_by("price").reverse()
        elif price and chesubcat==None and order and brand:
            if order=="priceLower":
                response=Product.objects.brandxprice(brand,price).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.brandxprice(brand,price).order_by("price").reverse()
        
       
        
        
        elif price==None and chesubcat==None and order==None and brand==None:
            response=Product.objects.values("id","name","price","marca__name","slug","image")
        elif price==None and chesubcat and order and brand==None:
            if order=="priceLower":
                response=Product.objects.get_category_product(chesubcat).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.get_category_product(chesubcat).order_by("price").reverse()           
        elif price==None and chesubcat and brand and order:
            if order=="priceLower":
                response=Product.objects.catxbrand(chesubcat,brand).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.catxbrand(chesubcat,brand).order_by("price").reverse()
        elif price==None and order and brand and chesubcat==None: 
            if order=="priceLower":
                response=Product.objects.get_brands_product(brand).order_by("price")
            elif order=="priceHigher":
                response=Product.objects.get_brands_product(brand).order_by("price").reverse()      
        elif price==None and order==None and brand and chesubcat:
            response=Product.objects.catxbrand(chesubcat,brand)
        elif price==None and order==None and brand and chesubcat==None:
            response=Product.objects.get_brands_product(brand)
        elif price==None and order==None and brand==None and chesubcat:
            response=Product.objects.get_category_product(chesubcat)
        elif price==None and order and brand==None and chesubcat==None:
            if order=="priceLower":
                response=Product.objects.order_by("price")
            elif order=="priceHigher":
                response=Product.objects.order_by("price").reverse()
       
    post = Paginator(response,4)
    if(request.GET.get("page")):
        page_obj = post.page(request.GET.get("page"))  
    else:
        page_obj = post.page(1)
            
    context={"product":page_obj,"text":'Nuestros productos.',"tag":"Productos","productActive":"active"}
    return render(request,"productList.html",context)


def byCategory(request,id,slug):
    if request.method=="GET":
        brand=request.GET.get("brand")
        order=request.GET.get("order")
        node = Category.objects.get(id=id)
        price=request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        if node.is_child_node():
            category=Product.objects.values("id","slug","name","price","marca__name","image").filter(category=node)
        else:
            category=Product.objects.values("id","slug","name","price","marca__name","image").filter(category__parent=node.get_root().id)  
        if price and brand==None and order==None :
            context=category.filter(price__lt=price[1],price__gt=price[0])  
        elif price and brand and order==None:
            context=category.filter(marca__name=brand,price__lt=price[1],price__gt=price[0])    
        elif price and brand and order:
            if order=="priceLower":
                context=category.filter(marca__name=brand,price__lt=price[1],price__gt=price[0]).order_by("price")
            elif order=="priceHigher":
                context=category.filter(marca__name=brand,price__lt=price[1],price__gt=price[0]).order_by("price").reverse()          
        elif price and brand==None and order:
            if order=="priceLower":
                context=category.filter(price__lt=price[1],price__gt=price[0]).order_by("price")    
            elif order=="priceHigher":
                context=category.filter(price__lt=price[1],price__gt=price[0]).order_by("price").reverse()
        elif price and brand and order==None:
            context=category.filter(marca__name=brand,price__lt=price[1],price__gt=price[0])

        elif price==None and order==None and brand==None:
            context=category    
        elif price==None and order==None and brand:
            context=category.filter(marca__name=brand)
        elif price==None and order and brand==None:
            if order=="priceLower" :
                context=category.order_by("price")
            elif order=="priceHigher":
                context=category.order_by("price").reverse()
        elif price==None and order and brand:
            if order=="priceLower" :
                context=category.filter(marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=category.filter(marca__name=brand).order_by("price").reverse()
        post = Paginator(context,1)
        if(request.GET.get("page")):
            page_obj = post.page(request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return render(request,"productList.html",{"product":page_obj ,"tag":"Productos","tag2":node,"displayCat":"none"})
class byMarcas(TemplateView):
    template_name="productList.html"
    def get(self,request,*args, **kwargs):
        subcat=request.GET.get("sc")
        marca = kwargs['id']
        order=request.GET.get("order")
        price=request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        if subcat==None or subcat=="":
            pass
        else:
            subcat=subcat.split(",")
        marcas=Product.objects.values("id","slug","name","price","marca__name","image").filter(marca=marca)

        if price and subcat==None and order==None :
            context=marcas.filter(price__lt=price[1],price__gt=price[0])  
        elif price and subcat and order==None:
            context=marcas.filter(category__in=subcat,price__lt=price[1],price__gt=price[0])    
        elif price and subcat and order:
            if order=="priceLower":
                context=marcas.filter(category__in=subcat,price__lt=price[1],price__gt=price[0]).order_by("price")
            elif order=="priceHigher":
                context=marcas.filter(category__in=subcat,price__lt=price[1],price__gt=price[0]).order_by("price").reverse()          
        elif price and subcat==None and order:
            if order=="priceLower":
                context=marcas.filter(price__lt=price[1],price__gt=price[0]).order_by("price")    
            elif order=="priceHigher":
                context=marcas.filter(price__lt=price[1],price__gt=price[0]).order_by("price").reverse()
        elif price and subcat and order==None:
            context=marcas.filter(category__in=subcat,price__lt=price[1],price__gt=price[0])  
        elif price==None and order==None and subcat :
            context=marcas.filter(category__in=subcat)
        elif price==None and order==None and subcat==None:
            context=marcas
        elif price==None and order and subcat ==None:
            if order=="priceLower":
                context=marcas.order_by("price")
            elif order=="priceHigher":
                context=marcas.order_by("price").reverse()
        elif price==None and order and subcat:
            if order=="priceLower":
                context=marcas.filter(category__id__in=subcat).order_by("price")
            elif order=="priceHigher":
                context=marcas.filter(category__id__in=subcat).order_by("price").reverse()

        post = Paginator(context,1)
        if(request.GET.get("page")):
            page_obj = post.page(request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return render(request,self.template_name,{"product":page_obj ,"tag":"Productos","tag2":marca,"productActive":"active","displayBrand":"none"})


def getProduct(request,pk):
    if request.method == 'GET':
        item=Product.objects.get(id=pk)
        with connection.cursor() as cursor:
            cursor.execute("select * from nRatings("+str(pk)+")")
            row = cursor.fetchone() 
        print(row)
        data = {
                'response': render_to_string("modal.html", {'product': item,"n":row[0]}, request=request)}
        return JsonResponse(data,safe=False)
class Search(TemplateView):
    template_name="productList.html"

    def get(self,request,*args, **kwargs):
        search=request.GET.get("q")
        brand=request.GET.get("brand")
        categ=request.GET.get("sc")
        order=request.GET.get("order")
      
        if categ==None or categ=="":
            categ=categ
        else:
            categ=categ.split(",")
        price=request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        searchby=Product.objects.values("id","slug","name","price","marca__name","image")
        if price and order==None and brand==None and categ and search=="":
            context=searchby.filter(price__lt=price[1],price__gt=price[0],category__in=categ)
        elif price and order==None and search=="" and brand and categ:
            context=searchby.filter(marca__name=brand,category__in=categ,price__lt=price[1],price__gt=price[0])
        elif price and order==None and search=="" and  brand==None and categ:    
            context=searchby.filter(price__lt=price[1],price__gt=price[0],category__in=categ)
        elif price and order==None and search=="" and brand and categ==None :
            context=searchby.filter(price__lt=price[1],price__gt=price[0],marca__name=brand)
        elif price and order==None and search and brand==None and categ :
            context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,category__in=categ)      
        elif price and order==None and search and brand==None and (categ==None or categ=="") :
            context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search)       
        elif price and order==None and search and (categ=="" or categ==None)  and brand :
            context=searchby.filter(price__lt=price[1],price__gt=price[0],marca__name=brand,name__icontains=search)
        elif price and order==None and search and categ  and brand :
            context=searchby.filter(price__lt=price[1],price__gt=price[0],marca__name=brand,name__icontains=search,category__in=categ)

        elif  price and order and search=="" and categ   and brand:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],category__in=categ,marca__name=brand).order_by("price").reverse() 
        elif  price and order and search and (categ=="" or categ==None)  and brand:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,marca__name=brand).order_by("price").reverse()  

        elif price and order and search and (categ=="" or categ==None)  and brand==None:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search).order_by("price").reverse()       

        elif  price and order and search and categ and brand:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,category__in=categ,marca__name=brand).order_by("price").reverse()   
        elif  price and order and search=="" and categ==None and brand:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],marca__name=brand).order_by("price").reverse()           
        elif price and  order and search and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,category__in=categ).order_by("price").reverse() 
        elif  price and order and search=="" and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0],category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(category__in=categ).order_by("price").reverse()           
        elif  price and order and search=="" and brand==None and (categ =="" or categ==None):
            if order=="priceLower":
                context=searchby.filter(price__lt=price[1],price__gt=price[0]).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(price__lt=price[1],price__gt=price[0]).order_by("price").reverse()   
        
        elif price==None and  order==None and brand==None and (categ==None or categ=="") and search=="":
            context=searchby
        elif price==None and  order==None and search=="" and brand and categ :
            context=searchby.filter(marca__name=brand,category__in=categ)
        elif price==None and  order==None and search=="" and  brand==None and categ:    
            context=searchby.filter(category__in=categ)
        elif price==None and  order==None and search=="" and brand and categ==None :
            context=searchby.filter(marca__name=brand)
        elif price==None and  order==None and search and brand==None and categ :
            context=searchby.filter(name__icontains=search,category__in=categ)      
        elif price==None and  order==None and search and brand==None and (categ==None or categ=="") :
            context=searchby.filter(name__icontains=search)       
        elif price==None and  order==None and search and (categ=="" or categ==None)  and brand :
            context=searchby.filter(marca__name=brand,name__icontains=search)
        elif price==None and order==None and search and categ  and brand :
            context=searchby.filter(marca__name=brand,name__icontains=search,category__in=categ)
        elif  price==None and  order and search=="" and categ   and brand:
            if order=="priceLower":
                context=searchby.filter(category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(category__in=categ,marca__name=brand).order_by("price").reverse() 
        elif price==None and   order and search and (categ=="" or categ==None)  and brand:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,marca__name=brand).order_by("price").reverse()  
        elif price==None and   order and search and (categ=="" or categ==None)  and brand==None:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search).order_by("price").reverse()                     
        elif price==None and   order and search and categ and brand:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,category__in=categ,marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,category__in=categ,marca__name=brand).order_by("price").reverse()   
        elif price==None and  order and search=="" and categ==None and brand:
            if order=="priceLower":
                context=searchby.filter(marca__name=brand).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(marca__name=brand).order_by("price").reverse()           
        elif price==None and  order and search and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(name__icontains=search,category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(name__icontains=search,category__in=categ).order_by("price").reverse() 
        elif price==None and  order and search=="" and categ  and brand==None:
            if order=="priceLower":
                context=searchby.filter(category__in=categ).order_by("price")
            elif order=="priceHigher":
                context=searchby.filter(category__in=categ).order_by("price").reverse()           
        elif price==None and  order and search=="" and brand==None and (categ =="" or categ==None) :
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
