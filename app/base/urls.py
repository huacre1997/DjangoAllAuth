from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import *
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name="index"),
    path('sobre-nosotros', AboutView.as_view(), name="about"),
    path('contactanos', ContactView.as_view(), name="contact"),

    path('login',LoginFormView.as_view(),name="login"),
    path('signup',RegisterView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(next_page="/"),name="logout"),
    path("province/",getProvince,name="getprovince"),
    path("district/",getDistrict,name="getdistrict"),

    # path('activate/<uidb64>/<token>/',activate, name='activate'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)    
