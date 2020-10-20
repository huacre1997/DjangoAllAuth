from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from django.views.generic import FormView,TemplateView


from allauth.account.decorators import verified_email_required
from allauth.account.views import LoginView,SignupView


from  accounts.models import  CustomCliente

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm
from accounts.forms import MyCustomSignupForm
from django.views.decorators.csrf import csrf_exempt
import json
UserModel = get_user_model()
from allauth.account.admin import EmailAddress
class IndexView(TemplateView):
    template_name = "index.html"


class RegisterView(SignupView):
    form_class=MyCustomSignupForm
    def post(self,request,*args, **kwargs):
        data={}
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            data = {
                'stat': True,
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
            return JsonResponse(data)
        else :
            data = {
                "error":form.errors,
                'stat': False,
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
            return JsonResponse(data)
        return HttpResponse('Activation link is valid!')

class LoginFormView(LoginView):
    form_class = LoginForm
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print("Entro al post")
        data = {}
        form = LoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            print("form valido")
            username = request.POST['login']
            password = request.POST['password']        
            user = authenticate(request, username=username, password=password) 
            if EmailAddress.objects.filter(user=user, verified=False).exists():
                print("Email verified")
                data = {
                "error":"Su cuenta aún no se encuentra activada.",
                'stat': False}
                return JsonResponse(data)
            

            if user is not None:
                print("User none")
                login(request, user)
                data = {
                'stat': True}
            else:
                print("None")
            return JsonResponse(data)
        else:
            print("else")
            data = {
                "error":form.errors["__all__"][0],
                'stat': False,
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
            return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        context["login"]=LoginForm
        return context
