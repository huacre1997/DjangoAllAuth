from django.urls import path,include
from .views import CheckOutView, editName
urlpatterns=[
    path("checkout/",CheckOutView.as_view(),name="checkout"),
    path("editData/",editName,name="edit_data"),

]