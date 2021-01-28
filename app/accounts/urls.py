from django.urls import path,include
from .views import *


urlpatterns = [
    path("profile/",ProfileView.as_view(),name="profile"),
    path("change_password/",change_password,name="change_password"),
    path("editData/",editName,name="edit_data"),
    path("createAddress/",createAddress,name="createAddress")

]