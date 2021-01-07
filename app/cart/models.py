from django.db import models
from app.settings import AUTH_USER_MODEL
from django.apps import apps

from products.models import Product

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
class Cart(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
 
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
    if not instance._state.adding:
        print ('this is an update')
    else:
        print ('this is an insert')
    if not kwargs["created"]:
        print("no created")
        count=instance.count-instance.cart.quantity
        line_cost = (instance.count-instance.cart.quantity) * instance.product.price
        
    else:    
        print("creted")   
        count=instance.count

        line_cost = instance.count * instance.product.price
    instance.cart.total = Decimal(instance.cart.total) + line_cost

    instance.cart.quantity += count
    instance.updated = datetime.now()

    instance.cart.save()