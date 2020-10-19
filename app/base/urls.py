from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth.views import LogoutView,FormView
from base.views import IndexView
from django.conf.urls.static import static
# from .views import LogoutView,LoginFormView,RegisterView,activate,LoginView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    # path('accounts/login/',LoginFormView.as_view(),name="login"),
    # path('logout/',LogoutView.as_view(next_page="/"),name="logout"),
    # path('accounts/signup/',RegisterView.as_view(),name="register"),
    # path('activate/<uidb64>/<token>/',activate, name='activate'),
]
