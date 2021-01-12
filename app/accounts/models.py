from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractUser, User
from django.db.models.base import Model
from app.settings import AUTH_USER_MODEL

class Province(models.Model):
    name = models.CharField(max_length=50)
class District(models.Model):
    provincia = models.ForeignKey(Province, related_name='provincia_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False)

class CustomCliente(AbstractUser):
    REQUIRED_FIELDS = []
    
    dni=models.CharField(verbose_name="DNI",max_length=8)
    celular=models.CharField(verbose_name="Celular",max_length=9)
    fechanac=models.DateField(verbose_name="Fecha de nacimiento",null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email

class Adress(models.Model):
    user=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    refrences = models.CharField(max_length=100, blank=True, null=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    province=models.ForeignKey(Province,on_delete=models.CASCADE)
    @property
    def getNameProvince(self):
        return self.province.name
    @property
    def getNameDistrict(self):
        return self.district.name