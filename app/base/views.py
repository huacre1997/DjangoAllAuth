from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,TemplateView
from allauth.account.views import LoginView,SignupView
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm
from accounts.forms import MyCustomSignupForm
import json
from allauth.account.admin import EmailAddress
from products.models import Category,Marcas,Product,Productimage
from django.urls import reverse
from django.template import RequestContext 
from django.views import generic

class IndexView(TemplateView):
    template_name="index.html"
    
def handler404(request, exception, template_name="base/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

# class IndexView(TemplateView):
#     template_name="index.html"
#     def get(self,request,*args, **kwargs):
#         data=[]
#         for i in SubCategory.objects.all():
#             data.append(i.toJSON())
#         return render(request, self.template_name, {'obj': data})


    
class RegisterView(SignupView):
    form_class=MyCustomSignupForm
    def post(self,request,*args, **kwargs):
        data={}
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            self.user = form.save(self.request)
            try:
                return complete_signup(
                    self.request,
                    self.user,
                    app_settings.EMAIL_VERIFICATION,
                    None,
                )
            except ImmediateHttpResponse as e:
                return e.response
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
