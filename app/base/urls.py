from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from base.views import *
from django.conf.urls.static import static
from .views import LoginFormView,RegisterView,LoginView

from django.contrib.auth.views import LogoutView
handler404 = 'base.views.handler404' 

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('sobre-nosotros', AboutView.as_view(), name="about"),
    path('contactanos', ContactView.as_view(), name="contact"),

    path('login',LoginFormView.as_view(),name="login"),
    path('signup',RegisterView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(next_page="/"),name="logout"),
    
    # path('activate/<uidb64>/<token>/',activate, name='activate'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)    
