from django.db import models
from app.settings import AUTH_USER_MODEL
from django.apps import apps

from products.models import Product

class CartManager(models.Manager):
    
    def amount(self,user):
        total=0
        d= self.get_queryset().filter(user=user)
  
        for i in d:
            total+=i.quantity
        return total
class Cart(models.Model):
    user        = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    product     = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity    = models.IntegerField()
    updated     = models.DateTimeField(auto_now=True)
    created   = models.DateTimeField(auto_now_add=True)
    objects=CartManager()

    @property
    def brand(self):
        return self.product.marca
    @property
    def price(self):
        return self.product.price
    @property
    def image(self):
        return self.product.image.url
    def total(self):
        return self.quantity*self.product.price
   
      
    def total(self,user):
        total=0
        d=self.objects.filter(user=user)
        for i in d:
            total+=i.quantity*i.product.price
        return total