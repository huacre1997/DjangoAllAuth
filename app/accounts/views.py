from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import CustomCliente,Adress, District, Province
from .forms import ChangePassword
import json
from .forms import AdressForm

class ProfileView(DetailView):
    model = CustomCliente
    template_name = "profile.html"
    context_object_name = 'obj'
    def get_object(self):
        if 'pk' not in self.kwargs:
            print(self.request.user.id)
            return CustomCliente.objects.get(id=self.request.user.id)
        return super(ProfileView, self).get_object()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ChangePassword()
        context["address"]=Adress.objects.filter(user=self.request.user.id)
        return context
from django.contrib.auth import update_session_auth_hash

def change_password(request):
    if request.method == 'POST':

        data={}
        form=ChangePassword(user=request.user,data=request.POST)
        if form.is_valid():
            data=CustomCliente.objects.get(id=request.user.id)
            data.set_password(form.cleaned_data["new_pass"])
            data.save()
            update_session_auth_hash(request, data)

            return JsonResponse({"response":"ok"},safe=False)

        else:
            data = {
                    "error":form.errors,
                    'stat': False,
                    }
            return JsonResponse(data)
    
def editName(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        data=CustomCliente.objects.get(id=request.user.id)
        data.first_name=post["name"]
        data.last_name=post["last"]
        data.save()
    return JsonResponse({"response":"ok"},safe=False)

def createAddress(request):
    if request.method=="POST":
        form=AdressForm(request.POST)  

        if request.POST["method_address"]=="post":
            
            if form.is_valid():  
                data=Adress()
                data.user_id=request.user.id
                data.description=form.cleaned_data["description"]
                data.refrences=form.cleaned_data["refrences"]
                data.district=form.cleaned_data["district"]
                data.province=form.cleaned_data["province"]
            
                data.save()
                print("id")
                return JsonResponse({"id":data.id,"province":data.province.name,"district":data.district.name,"description":data.description,"refrences":data.refrences},safe=False)
                    
            else:
                return HttpResponse(form.errors)
        else:
            print(request.POST)
            data=Adress.objects.get(id=request.POST["address_profile"])
            province=Province.objects.get(id=request.POST["province"])
            district=District.objects.get(id=request.POST["district"])

            data.description=request.POST["description"]
            data.refrences=request.POST["refrences"]
            data.district=district
            data.province=province
            data.save()
            return JsonResponse({"response":"edit"},safe=False)
