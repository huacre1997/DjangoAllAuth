from django.urls import path,include
from .views import CheckOutView,charges
urlpatterns=[
    path("checkout/",CheckOutView.as_view(),name="checkout"),
    path("charges/", charges, name='charges'),

]