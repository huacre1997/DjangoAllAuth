from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import *
from django.conf.urls.static import static



urlpatterns = [
    # path('', ProductsView, name="productView"),
     path('<str:cat>',getCat.as_view(),name="getCat"),
     path('subcategory/<str:cat>',getCat.as_view(),name="getCatList"),
     path('products/',ProductList,name="getProducList"),
    # path('products/filter',filterProduct.as_view(),name="filterProduct"),
     path('products/search/<int:id>',getProduct,name="getProductDetail"),
     path('products/',filter,name="filterProduct"),

    # path('products/',getFiltered,name="filterProduct"),
    # path('<str:tipo>/<str:slug>',filterProductAll.as_view(),name="filterProductAll"),

    
    #  path('marca/<str:marca>',getMarcas.as_view(),name="getMarcas"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
