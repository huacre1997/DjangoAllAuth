from django.db import models
from base.models import BaseModel
from crum import get_current_user
from django.forms.models import model_to_dict
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.db.utils import IntegrityError

from mptt.models import MPTTModel, TreeForeignKey

from django.dispatch import receiver
from easy_thumbnails.signals import saved_file
from products import tasks

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global


class Category(MPTTModel):
    name = models.CharField(verbose_name="Nombre Categoría",max_length=100)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children2')
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    
    def clean_slug(self):
        return self.cleaned_data["slug"]
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
    class MPTTMeta:
        order_insertion_by=['name']

class Marcas(BaseModel):
    name=models.CharField(verbose_name="Nombre de la Marca", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        self.slug = slugify(self.name)
        super(Marcas, self).save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
from django.db.models import Q
from django.urls import reverse

class ProductQuerySet(models.QuerySet):
    def catxbrand(self,category,brand):
        return self.values("id","name","marca__name","price","image","slug").filter(category__in=category.split(","),marca__name=brand)  
    def catxprice(self,category,price):
        return self.values("id","name","marca__name","price","image","slug").filter(category__in=category.split(","),price__lt=price[1],price__gt=price[0])  
    def brandxprice(self,brand,price):
        return self.values("id","name","marca__name","price","image","slug").filter(marca__name=brand,price__lt=price[1],price__gt=price[0])  
    def filterMultiple(self,category,brand,price):
        return self.values("id","name","marca__name","price","image","slug").filter(category__in=category.split(","),marca__name=brand,price__lt=price[1],price__gt=price[0])  
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)
    def get_brands_product(self,brand):
        return self.get_queryset().values("id","name","marca__name","price","image","slug").filter(marca__name=brand).distinct()
    def get_price_product(self,price):
        return self.values("id","name","marca__name","price","image","slug").filter(price__lt=price[1],price__gt=price[0])    
    def get_category_product(self,category):
        return self.get_queryset().values("id","name","marca__name","price","image","slug").filter(category__in=category.split(",")).distinct()   
    def orderLower(self):
        return self.get_queryset().values("id","name","marca__name","price","image","slug").order_by("price")
    def orderHigher(self):
        return self.get_queryset().values("id","name","marca__name","price","image","slug").order_by("price").reverse()
    def filterMultiple(self,category,brand,price):
        return self.get_queryset().filterMultiple(category,brand,price) 
    def catxbrand(self,category,brand):
        return self.get_queryset().catxbrand(category,brand) 
    def catxprice(self,price,category):
        return self.get_queryset().catxprice(category,price) 
    def brandxprice(self,brand,price):
        return self.get_queryset().brandxprice(brand,price) 

from PIL import Image
from io import BytesIO
from django.core.files import File
class Product(BaseModel):
    name=models.CharField("Nombre del producto", max_length=50)
    sku = models.CharField(max_length=50) 
    price = models.DecimalField("Precio",max_digits=9,decimal_places=2)   
    before = models.DecimalField("Precio anterior",max_digits=9,decimal_places=2,blank=True)   
    category=TreeForeignKey("Category", verbose_name="Categoría", on_delete=models.CASCADE,related_name="children") 
    marca=models.ForeignKey(Marcas, verbose_name="Marcas del producto", on_delete=models.CASCADE,related_name="marca_id")
    descripcion=models.CharField(verbose_name="Descripcion",max_length=200,default="")
    caracteristicas= RichTextField(blank=True,null=True)
    modelo=models.CharField("Modelo",max_length=50)
    amount=models.IntegerField("Stock")
    slug = models.SlugField(max_length=255, unique=True,help_text='Unique value for product page URL, created from name.') 
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag')
    image=models.ImageField("Imagen Principal",blank=True,upload_to="uploads/")
    rating=models.FloatField(default=0)
    objects=ProductManager()
    @property
    def get_absolute_url(self):      
        return reverse('products:product_detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        self.slug = slugify(self.name)
        self.meta_keywords = self.name
        self.meta_description = self.descripcion

        super(Product, self).save(*args, **kwargs)
    class Meta:
        verbose_name ="Producto"
        verbose_name_plural = "Productos"
        ordering=["-created"]
    def __str__(self):
        return self.name
 
    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['marca'] = self.marca.toJSON()
        item["image"]=self.image.url
        item["price"]=format(self.price,".2f")
        return item
    def updateRate(self,val):
        self.rating=val
        self.save()
class Productimage(models.Model):
    product=models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images/")

    def __str__(self):
        return self.product.name

class Comment(models.Model):
    STATUS=(("Nuevo","Nuevo"),("True","True"),("False","False"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=30)
    comment = models.TextField(max_length=200)
    rate=models.IntegerField(default=1)
    ip=models.CharField(max_length=20,blank=True)
    created_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS,default="New")


    def __str__(self):
        return self.comment
