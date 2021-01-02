from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('productos/<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),

    path('marcas/<slug:marca>/', byMarcas.as_view(), name="byMarcas"),
    path('marcas/<slug:marca>/<slug:slug>/', ProductDetailView.as_view(), name="product_detail_brand"),

    path('categorias/<slug:categoria>/', byCategory.as_view(), name="byCategory"),
    path('categorias/<slug:categoria>/<slug:slug>/', ProductDetailView.as_view(), name="product_detail_category"),

    path('productos/', cache_page(60 * 15)(ProductList.as_view()), name="getProducList"),
    path('productos/search/<int:pk>', getProduct, name="getProductDetail"),
    path('productos/search', Search.as_view(), name="search"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
