from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialAccountSign

from django import forms
from django.forms import *
from accounts.models import CustomCliente
from allauth.socialaccount import forms
from datetime import datetime
class MyCustomSignupForm(SignupForm):
    
    first_name=CharField( max_length=20, required=True)
    last_name=CharField( max_length=20, required=True)
    dni = CharField(max_length=8,label="Dni",required=True)
    celular = CharField(max_length=9,label="Celular",required=True)
    fechanac = DateField(label="Fecha de nacimiento")

    class Meta:
        model = CustomCliente
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
    
    def clean_fechanac(self):
        fechanac = self.cleaned_data['fechanac']
        edad=int((datetime.now().date() - fechanac).days / 365.25)  
        if edad<18:
            raise ValidationError("Debe ser mayor de edad")
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if CustomCliente.objects.filter(dni=dni).exists():
            raise ValidationError("El dni ya se encuentra registrado.")
        return dni
    def clean_celular(self):
        celular = self.cleaned_data['celular']
        if CustomCliente.objects.filter(celular=celular).exists():
            raise ValidationError("El celular ya se encuentra registrado.")
        return celular
    
    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.dni = self.cleaned_data['dni']
        user.celular = self.cleaned_data['celular']
        user.fechanac =self.cleaned_data['fechanac']
        user.save()
        return user
class MyCustomSocialSignupForm(SocialAccountSign):
    dni = CharField(max_length=8,label="Dni",required=True)
    celular = CharField(max_length=9,label="Celular",required=True)
    fechanac = DateField(label="Fecha de nacimiento")
  
    class Meta:
        model = CustomCliente
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
       
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if CustomCliente.objects.filter(dni=dni).exists():
            raise ValidationError("El dni ya se encuentra registrado.")
        return dni
    def clean_celular(self):
        celular = self.cleaned_data['celular']
        if CustomCliente.objects.filter(celular=celular).exists():
            raise ValidationError("El celular ya se encuentra registrado.")
        return celular
    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.dni = self.cleaned_data['dni']
        user.celular = self.cleaned_data['celular']
        user.fechanac =self.cleaned_data['fechanac']
        user.save()
        return user