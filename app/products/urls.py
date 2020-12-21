from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page



urlpatterns = [
    # path('', ProductsView, name="productView"),
     path('products/<int:id>/<str:slug>/',byCategory,name="byCategory"),
     path('products/<int:id>/<str:marca>',byMarcas.as_view(),name="byMarcas"),

     path('products/',cache_page(60 * 15)(ProductList.as_view()),name="getProducList"),
    # path('products/filter,filterProduct.as_view(),name="filterProduct"),
     path('products/search/<int:pk>',getProduct,name="getProductDetail"),
     path('products/search',Search.as_view(),name="search"),
     path('products/<str:slug>',ProductDetailView.as_view(),name="product_detail"),

    # path('products/',getFiltered,name="filterProduct"),
    # path('<str:tipo>/<str:slug>',filterProductAll.as_view(),name="filterProductAll"),

    
    #  path('marca/<str:marca>',getMarcas.as_view(),name="getMarcas"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
