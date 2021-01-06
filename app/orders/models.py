# from django.db import models
# from django.db.models import Sum
# from django.conf import settings
# from django.urls import reverse
# from django.dispatch import receiver
# from django.db.models.signals import post_delete
# from app.settings import AUTH_USER_MODEL
# from django.apps import apps

# from decimal import Decimal
# modelCart = apps.get_model('cart', 'Cart')

# modelProduct = apps.get_model('products', 'Product')
# ORDER_STATUS_CHOICES = (
#     ('creado', 'Creado'),
#     ('pagado', 'Pagado'),
#     ('enviado', 'Enviado'),
#     ('reembolsado', 'Reembolsado'),
# )

# class Order(models.Model):
#     customer            = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
#     order_id            = models.CharField(max_length=120, blank=True) # AB31DE3
#     cart                = models.ForeignKey(modelCart)
#     status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
#     total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
#     active              = models.BooleanField(default=True)
#     updated             = models.DateTimeField(auto_now=True)
#     timestamp           = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.order_id

#     objects = OrderManager()

#     class Meta:
#        ordering = ['-timestamp', '-updated']

#     def get_absolute_url(self):
#         return reverse("orders:detail", kwargs={'order_id': self.order_id})

#     def get_status(self):
#         if self.status == "refunded":
#             return "Refunded order"
#         elif self.status == "shipped":
#             return "Shipped"
#         return "Shipping Soon"

#     def update_total(self):
#         cart_total = self.cart.total
#         shipping_total = self.shipping_total
#         new_total = math.fsum([cart_total, shipping_total])
#         formatted_total = format(new_total, '.2f')
#         self.total = formatted_total
#         self.save()
#         return new_total

#     def check_done(self):
#         shipping_address_required = not self.cart.is_digital
#         shipping_done = False
#         if shipping_address_required and self.shipping_address:
#             shipping_done = True
#         elif shipping_address_required and not self.shipping_address:
#             shipping_done = False
#         else:
#             shipping_done = True
#         billing_profile = self.billing_profile
#         billing_address = self.billing_address
#         total   = self.total
#         if billing_profile and shipping_done and billing_address and total > 0:
#             return True
#         return False

#     def update_purchases(self):
#         for p in self.cart.products.all():
#             obj, created = ProductPurchase.objects.get_or_create(
#                     order_id=self.order_id,
#                     product=p,
#                     billing_profile=self.billing_profile
#                 )
#         return ProductPurchase.objects.filter(order_id=self.order_id).count()

#     def mark_paid(self):
#         if self.status != 'paid':
#             if self.check_done():
#                 self.status = "paid"
#                 self.save()
#                 self.update_purchases()
#         return self.status

