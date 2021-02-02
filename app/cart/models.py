from django.db import models
from app.settings import AUTH_USER_MODEL
from django.apps import apps

from products.models import Product

from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
class CartManager(models.Manager):
    def get_Total(self, user):
        
        return self.model.objects.get(user=user)
class Cart(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    objects=CartManager()
class CartItem(models.Model):
    product     = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    count    = models.PositiveIntegerField()
    updated     = models.DateTimeField(auto_now=True)
    created   = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    
    @property
    def price(self):
        return self.product.price
    @property
    def image(self):
        return self.product.image.url
    def total(self):
        return self.count*self.product.price
  

from decimal import Decimal

@receiver(post_save, sender=CartItem)
def update_cart(sender, instance, **kwargs):
   
    if kwargs["created"]:
        print("creato")
    else:
        print("update")
    if instance.count==0:
        instance.delete()
    line_cost = instance.count * instance.product.price
    instance.cart.total = Decimal(instance.cart.total) + line_cost

    instance.cart.quantity += instance.count
    instance.updated = datetime.now()

    instance.cart.save()

@receiver(post_delete, sender=CartItem)
def delete_cart(sender, instance, **kwargs):
   

    line_cost = instance.count * instance.product.price
    instance.cart.total = instance.cart.total- line_cost

    instance.cart.quantity =instance.cart.quantity- instance.count
  

    instance.cart.save()