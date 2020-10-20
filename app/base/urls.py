from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from base.views import IndexView
from django.conf.urls.static import static
from .views import LoginFormView,RegisterView,LoginView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login',LoginFormView.as_view(),name="login"),
    path('signup',RegisterView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(next_page="/"),name="logout"),

    # path('activate/<uidb64>/<token>/',activate, name='activate'),
]
