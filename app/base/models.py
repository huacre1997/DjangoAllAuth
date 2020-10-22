from django.db import models

from django.contrib.auth.models import AbstractUser
from app.settings import AUTH_USER_MODEL
from django.conf import settings
class BaseModel(models.Model):

    status=models.BooleanField(verbose_name="Estado",default=True,blank=False)

    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,default=None,on_delete=models.CASCADE,related_name="+",verbose_name="Creado por")
    modified = models.DateTimeField(auto_now=True,verbose_name="Fecha de modificación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,default=None,on_delete=models.CASCADE,related_name="+",verbose_name="Modificado por")
 


    class Meta:
        abstract = True

