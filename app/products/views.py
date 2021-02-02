from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from .models import *
from cart.models import CartItem,Cart
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
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from functools import reduce
from django.views.decorators.cache import never_cache
from cart.cart import Cart as ObjCart
class ProductDetailView(DetailView):
    model=Product
    template_name="product_detail.html"
    form_class=RatingForm
    @never_cache
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
 
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        queryset=Product.objects.select_related("category").all()
        return queryset
    def get_context_data(self, **kwargs):
        data=[]
        total,staravg=0,0
        context = super().get_context_data(**kwargs)
        q=Comment.objects.values("rate").filter(product=self.object.id).order_by("rate").reverse().annotate(Count('rate'))
        with connection.cursor() as cursor:
            cursor.execute("select * from getRating("+str(self.object.id)+") order by num")
            row = cursor.fetchall()       
        [ data.append(i[1]) for i in row]
        for k,i in enumerate(data):
            total+=i*(k+1)
        suma=reduce((lambda a,b: a+b),data) 
        if suma!=0: staravg=round(total/suma,1)
          
        context["starsAvg"]=staravg
        # current_url = resolve(self.request.path_info)
        context["starsCount"]=data[::-1]
        if "marca" in self.kwargs.keys():
            context["nameBrand"]=self.kwargs["marca"]
        if "categoria" in self.kwargs.keys():
            context["nameCategory"]=self.kwargs["categoria"]
        if self.request.user.is_authenticated:
            cartid=Cart.objects.values("id").filter(user_id= self.request.user.id)
  
            itemcart=CartItem.objects.filter(product_id=self.object.id,cart_id=cartid[0]["id"])
            if itemcart.exists():
                print("if auth")
                context["exists"]=1
               
        else:
            itemSession=ObjCart(self.request)
            val=itemSession.exists(self.object.id)
            if val:
                print("if session")

                context["exists"]=1


        # post = Paginator(Comment.objects.filter(product_id=self.object.id).order_by("created_date").reverse(),5)
        # if  self.request.GET.get('page'):
        #     page_obj = post.page( self.request.GET.get('page'))  
        # else:
        #     page_obj = post.page(1)
        context["image"] = Productimage.objects.filter(product=self.object.id)

        context["comment"]=Comment.objects.values("author__first_name","comment","created_date","rate").filter(product_id=self.object.id).order_by("created_date").reverse()
        return context
    def post(self, request, *args, **kwargs):
        if self.request.POST["paramSend"]=="next":
            print("if next")
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return HttpResponse(render_block_to_string(self.template_name,"content",context=context,request=self.request))

        else:
            if  request.user.is_authenticated: 
                print("if username")
                from crum import get_current_user          
                form=RatingForm(request.POST)    
                self.object = self.get_object()
                print(form)
                if form.is_valid():
                    data=Comment()
                    data.author=get_current_user()
                    data.comment=form.cleaned_data["comment"]       
                    data.ip=request.META.get("REMOTE_ADDR")
                    data.rate=form.cleaned_data["rate"]
                    data.product_id=self.object.id
                    data.save()
                    print("TOdo bien")
                    with connection.cursor() as cursor:
                        cursor.execute("select * from avgRating("+str(self.object.id)+")")
                        row = cursor.fetchone() 
                    self.object.updateRate(row[0])
                    context = self.get_context_data(**kwargs)
                    return self.render_to_response(context)   
                else:
                    print(form.errors)
                    return HttpResponse(form.errors)
            else:
                print("if not authenticated")

                return HttpResponse("No se encuentra logueado en el sistema")
from render_block import render_block_to_string

class ProductList(TemplateView):
    model=Product
    template_name="productList.html"
    @never_cache
    def dispatch(self, request, *args, **kwargs):
        return super(ProductList, self).dispatch(request, *args, **kwargs)
    
    def get(self,context,**kwargs):
        if self.request.GET:
            return render(self.request,self.template_name,self.getFilter())
        else:
            response =  Product.objects.values("id","name","price","before","rating","slug","image","created")
            post = Paginator(response, 3)
            if(self.request.GET.get("page")):
                page_obj = post.page(self.request.GET.get("page"))  
            else:
                page_obj = post.page(1)
            context={"entries":page_obj,"text":"Nuestros productos"}    
            return render(self.request,self.template_name,context)

    def getFilter(self,*args, **kwargs):
            # print(self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest')
            brand=self.request.GET.get("brand")
            order=self.request.GET.get("order")
            chesubcat=self.request.GET.get("sc")
            price=self.request.GET.get("price")
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
                response=Product.objects.values("id","name","price","before","rating","slug","image","created")
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
            post = Paginator(response, 3)
            if(self.request.GET.get("page")):
                page_obj = post.page(self.request.GET.get("page"))  
            else:
                page_obj = post.page(1)
            context={"entries":page_obj,"text":'Nuestros productos.'  }
            return context
    def post(self, request, *args, **kwargs) :
        
        return HttpResponse(render_block_to_string("productList.html","content",context=self.getFilter(),request=self.request))
        


class byCategory(ListView):
    template_name="productList.html"
    model=Category
    

    def get(self, request, *args, **kwargs) :
        if self.request.GET:
            return render(self.request,self.template_name,self.getCategory(kwargs["categoria"]))
        else:
            node = Category.objects.get(slug=kwargs["categoria"])

            if node.is_child_node():
                category=Product.objects.values("id","slug","name","price","rating","before","image").filter(category=node)
            else:
                category=Product.objects.values("id","slug","name","price","before","rating","image").filter(category__parent=node.get_root().id)  
            post = Paginator(category, 3)
            if(self.request.GET.get("page")):
                page_obj = post.page(self.request.GET.get("page"))  
            else:
                page_obj = post.page(1)
            context={"entries":page_obj,"text":"Nuestros productos","tag":2,"tag2":node.name,"displayCat":"none"}
         
            return render(self.request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        return HttpResponse(render_block_to_string("productList.html","content",context=self.getCategory(kwargs["categoria"]),request=self.request))


    def getCategory(self,slug):
        brand=self.request.GET.get("brand")
        order=self.request.GET.get("order")
        node = Category.objects.get(slug=slug)
        price=self.request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        if node.is_child_node():
            category=Product.objects.values("id","slug","name","price","before","rating","image").filter(category=node)
        else:
            category=Product.objects.values("id","slug","name","price","before","rating","image").filter(category__parent=node.get_root().id)  
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
        post = Paginator(context,3)
        if(self.request.GET.get("page")):
            page_obj = post.page(self.request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return {"entries":page_obj,"tag2":node.name,"displayCat":"none"}
       
class byMarcas(TemplateView):
    template_name="productList.html"
    def get(self,request,*args, **kwargs):
        if self.request.GET:
            return render(self.request,self.template_name,self.getMarca(kwargs["marca"]))
        else:
            marca=Marcas.objects.get(slug=kwargs["marca"])
            marcas=Product.objects.values("id","slug","name","price","before","rating","image").filter(marca=marca.id)
            post = Paginator(marcas, 1)
            if(self.request.GET.get("page")):
                page_obj = post.page(self.request.GET.get("page"))  
            else:
                page_obj = post.page(1)
            context={"entries":page_obj,"tag2":marca.name.lower(),"tag":3,"displayBrand":"none"}
         
            return render(self.request,self.template_name,context)
    def post(self, *args, **kwargs):
      
        return HttpResponse(render_block_to_string("productList.html","content",context=self.getMarca(kwargs["marca"]),request=self.request))

    def getMarca(self,slug):
        subcat=self.request.GET.get("sc")
        order=self.request.GET.get("order")
        price=self.request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        if subcat==None or subcat=="":
            pass
        else:
            subcat=subcat.split(",")
        marcas=Product.objects.values("id","slug","name","price","before","rating","image").filter(marca__slug=slug)

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
        if(self.request.GET.get("page")):
            page_obj = post.page(self.request.GET.get("page"))  
        else:
            page_obj = post.page(1)
        return {"entries":page_obj,"tag2":slug,"displayBrand":"none"}

from django.shortcuts import get_object_or_404

def getProduct(request,pk):
    if request.method == 'GET':
        item = get_object_or_404(Product, id=pk) 
        with connection.cursor() as cursor:
            cursor.execute("select * from nRatings("+str(pk)+")")
            row = cursor.fetchone() 
        data = {
                'response': render_to_string("modal.html", {'product': item,"n":row[0]}, request=request)}
        return JsonResponse(data,safe=False)
import re

class Search(TemplateView):
    
    template_name="productList.html"
    def get(self, *args, **kwargs):
        return render(self.request,self.template_name,self.results())
        
    def post(self, *args, **kwargs):
      
        return HttpResponse(render_block_to_string("productList.html","content",context=self.results(),request=self.request))

    def results(self):
        search_reg=self.request.GET.get("q")
        brand=self.request.GET.get("brand")
        categ=self.request.GET.get("sc")
        order=self.request.GET.get("order")
        
        patron = re.compile(r'[a-u]s\Z',re.I)
        if patron.search(search_reg)!=None:
            print("if")
            search=patron.sub("",search_reg)
        else:
            print("else")
            search=search_reg
      
        if categ==None or categ=="":
            categ=categ
        else:
            categ=categ.split(",")
        price=self.request.GET.get("price")
        if price==None:
            pass
        else:
            price=price.split(",")
        searchby=Product.objects.values("id","slug","name","price","rating","image")
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
                context=searchby.filter(price__lt=price[1],price__gt=price[0],name__icontains=search,category__in=categ,marca__name=brand).order_by("price").reverse()   
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
            print("only search")
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
        if(self.request.GET.get("page")):
            page_obj = post.page(self.request.GET.get("page"))  
        else:
            page_obj = post.page(1)
                
        context={"entries":page_obj,"tag3":search_reg}
        return context
