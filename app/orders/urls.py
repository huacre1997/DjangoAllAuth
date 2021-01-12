from django.urls import path,include
from .views import CheckOutView
urlpatterns=[
    path("checkout/",CheckOutView.as_view(),name="checkout")
]