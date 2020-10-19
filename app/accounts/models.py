from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from app.settings import AUTH_USER_MODEL

class CustomCliente(AbstractUser):
    REQUIRED_FIELDS = []
    
    dni=models.CharField(verbose_name="DNI",max_length=8)
    celular=models.CharField(verbose_name="Celular",max_length=9)
    fechanac=models.DateField(verbose_name="Fecha de nacimiento",null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.email

