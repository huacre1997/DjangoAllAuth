from allauth.account.forms import PasswordField, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialAccountSign

from django import forms as DjForm
from django.forms import *
from accounts.models import CustomCliente
from .models import Adress, District, Province
from allauth.socialaccount import forms
from datetime import datetime
from django.forms import ModelForm
from django.contrib.auth.models import User

class AdressForm(ModelForm):
    class Meta:
        model=Adress
        fields=["description","refrences","district","province"]
  
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
class ChangePassword(DjForm.Form):
    before_pass = PasswordField(max_length=100, required=True)
    new_pass = PasswordField(max_length=100, required=True)
    new_pass_repeat = PasswordField(max_length=100, required=True)
    user=None
    def __init__(self, *args, **kwargs):
        if kwargs:
            self.user = kwargs.pop('user')
        super(ChangePassword, self).__init__(*args, **kwargs)
    class Meta:
       
        widgets = {
             'before_pass': PasswordInput(render_value=True,attrs={
                "name": "before_pass",
                "id": "before_pass",
               
            }),
            'new_pass': PasswordInput(render_value=True,attrs={
                "name": "new_pass",
                "id": "new_pass",
                
            }),
            'new_pass_repeat': PasswordInput(render_value=True, attrs={
                "name": "new_pass_repeat",
                "id": "new_pass_repeat",
              
            })

        }

    def clean_before_pass(self):
        old_pass=self.cleaned_data["before_pass"]

        user = CustomCliente.objects.get(pk=self.user.id)
        print(user.password) 
        if not user.check_password(old_pass):
            raise ValidationError("Las contraseña ingresada no es correcta.")
     
        return old_pass
    def clean(self):
        cleaned_data = super(ChangePassword,self).clean()

        n_pass = cleaned_data.get("new_pass")
        r_pass = cleaned_data.get("new_pass_repeat")
       
        if r_pass != n_pass:
            raise ValidationError("Las contraseñas no coinciden.")

   
        return self.cleaned_data
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