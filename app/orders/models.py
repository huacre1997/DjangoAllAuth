from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
from app.settings import AUTH_USER_MODEL
from django.apps import apps
from cart.models import Cart
# from decimal import Decimal
from base.models import BaseModel

ORDER_STATUS_CHOICES = (
    ('creado', 'Creado'),
    ('pagado', 'Pagado'),
    ('enviado', 'Enviado'),
    ('reembolsado', 'Reembolsado'),
)
class Order(BaseModel):
    client            = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.order_id

#     objects = OrderManager()

    class Meta:
       ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

#     def get_status(self):
#         if self.status == "refunded":
#             return "Refunded order"
#         elif self.status == "shipped":
#             return "Shipped"
#         return "Shipping Soon"

    def update_total(self):
        cart_total = self.cart.total

        formatted_total = format(cart_total, '.2f')
        self.total = formatted_total
        self.save()
        return cart_total

