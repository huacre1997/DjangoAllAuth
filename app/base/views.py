from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,TemplateView
from allauth.account.views import LoginView,SignupView,EmailConfirmation
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
from django.template import RequestContext 
from accounts.models import Province,District,Adress
from django.core import serializers
from django.contrib.auth.views import LogoutView

def getProvince(request):
    qs=Province.objects.only("name","id")
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')
def getDistrict(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        qs=District.objects.filter(provincia_id=post)
        qs_json = serializers.serialize('json', qs)
        return HttpResponse(qs_json, content_type='application/json')
def index(request):

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    products =  Product.objects.values("id","name","price","before","rating","slug","image","created").order_by("created").reverse()
    offers =  Product.objects.values("id","name","price","before","rating","slug","image","created").filter(before__gte=0).order_by("created").reverse()
    top =  Product.objects.values("id","name","price","before","rating","slug","image","created").filter(rating__gte=4)

    context = {
        'num_visits': num_visits,
        "products":products,
        "offers":offers,
        "top":top
    }
    return render(request, 'index.html', context=context)
class AboutView(TemplateView):
    template_name="about.html"    
class ContactView(TemplateView):
    template_name="contact.html"
# def handler404(request, exception, template_name="base/404.html"):
#     response = render_to_response(template_name)
#     response.status_code = 404
#     return response

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
        print(request.POST)
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            self.user = form.save(self.request)
            try:
                mail=complete_signup(
                    self.request,
                    self.user,
                    app_settings.EMAIL_VERIFICATION,
                    None,
                )
         
                return JsonResponse({"mail": request.POST["email"] },safe=False)
            except ImmediateHttpResponse as e:
                return e.response
        else :
            data = {
                "error":form.errors,
                'stat': False,
                }
            return JsonResponse(data)

class LoginFormView(LoginView):
    form_class = LoginForm
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']        
            user = authenticate(request, username=username, password=password) 
            if EmailAddress.objects.filter(user=user, verified=False).exists():
                data = {
                "error":"Su cuenta aún no se encuentra activada.",
                'stat': False}
                return JsonResponse(data)
            

            if user is not None:
                login(request, user)
                data = {
                'stat': True}
            else:
                pass
            return JsonResponse(data)
        else:
            data = {
                "error":form.errors["__all__"][0],
                'stat': False,
                'form': render_to_string(self.template_name, {'form': form}, request=request)}
            return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context["title"] = "Login"
        context["login"]=LoginForm
        return context

