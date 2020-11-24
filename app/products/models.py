from django.db import models
from base.models import BaseModel
from crum import get_current_user
from django.forms.models import model_to_dict
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.db.utils import IntegrityError


from django.dispatch import receiver
from easy_thumbnails.signals import saved_file
from products import tasks

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global


class Category(BaseModel):
    name = models.CharField(verbose_name="Nombre Categoría",max_length=100)
    slug = models.SlugField(max_length=100)
    # meta_keywords = models.CharField('Meta Keywords',max_length=255)
    # meta_description = models.CharField("Meta Description", max_length=255) 
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
        print(self.cleaned_data["slug"])
        return self.cleaned_data["slug"]
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
class SubCategory(BaseModel):

    category=models.ForeignKey(Category, verbose_name="Categoría", on_delete=models.CASCADE,related_name="categoria_id")
    name = models.CharField(verbose_name="Nombre Subcategoría",max_length=100)
    slug = models.SlugField(max_length=100, unique=True,error_messages={
        'unique':"Ya ingresó esa subcategoria"
    })

    def save(self, *args, **kwargs):
    
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        self.slug = slugify(self.name)
    
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
     
    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        return item

    class Meta:
        verbose_name = 'SubCategoria'
        verbose_name_plural = 'SubCategorias'


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
class ProductQuerySet(models.QuerySet):
    def get_brands_product(self,brand):
        return self.values("id","name","marca__name","price","image").filter(marca__name=brand)
   
    def get_category_product(self,category):
        return self.values("id","name","marca__name","price","image").filter(subcategory__category__slug=category)
    def filterMultiple(self,subcategory,brand):
        return self.values("id","name","marca__name","price","image").filter(
    Q(subcategory__id__in=subcategory.split(",")) & Q(marca__name=brand)
)
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)
    def get_brands_product(self,brand):
        return self.get_queryset().get_brands_product(brand)
    def get_category_product(self,category):
        return self.get_queryset().get_category_product(category)
    def get_subcategory_product(self,subcategory):
        return self.get_queryset().values("id","name","marca__name","price","image").filter(subcategory__id__in=subcategory.split(","))   
    def orderLower(self):
        return self.get_queryset().values("id","name","marca__name","price","image").order_by("price")
    def orderHigher(self):
        return self.get_queryset().values("id","name","marca__name","price","image").order_by("price").reverse()
    def filterMultiple(self,subcategory,brand):
        return self.get_queryset().filterMultiple(subcategory,brand) 
from PIL import Image
from io import BytesIO
from django.core.files import File
class Product(BaseModel):
    name=models.CharField("Nombre del producto", max_length=50)
    sku = models.CharField(max_length=50) 
    price = models.DecimalField("Precio",max_digits=9,decimal_places=2)   
    before = models.DecimalField("Precio",max_digits=9,decimal_places=2,blank=True)   

    subcategory=models.ForeignKey(SubCategory, verbose_name="SubCategoria", on_delete=models.CASCADE,related_name="subcategoria_id") 
    marca=models.ForeignKey(Marcas, verbose_name="Marcas del producto", on_delete=models.CASCADE,related_name="marca_id")
    description= RichTextField(blank=True,null=True)
    modelo=models.CharField("Modelo",max_length=50)
    amount=models.IntegerField("Stock")
    slug = models.SlugField(max_length=255, unique=True,help_text='Unique value for product page URL, created from name.') 
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag')
    image=models.ImageField("Imagen Principal",blank=True,upload_to="uploads/")

    objects=ProductManager()

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    class Meta:
        verbose_name ="Producto"
        verbose_name_plural = "Productos"
        ordering=["-created"]
    def __str__(self):
        return self.name
   
    def toJSON(self):
        item = model_to_dict(self)
        item['subcategory'] = self.subcategory.toJSON()
        item['marca'] = self.marca.toJSON()
        item["image"]=self.image.url
        item["price"]=format(self.price,".2f")
        return item
    
class Productimage(models.Model):
    product=models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images/")

    def __str__(self):
        return self.product.name
@receiver(saved_file)
def generate_thumbnails_async(sender, fieldfile, **kwargs):
    tasks.generate_thumbnails.delay(
        model=sender, pk=fieldfile.instance.pk,
        field=fieldfile.field.name)