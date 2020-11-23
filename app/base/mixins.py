
from products.models import  *
from django.views import generic
from django.db.models import Count

class CustomMixin(generic.ListView):
    template_name="productList.html"
    model=Product
    # def get(self,request,*args, **kwargs):
    #     cat=[]
    #     subcat=[]
    #     marca=[]
    #     i=1
    #     k=1
    #     l=1
    #     category= Category.objects.annotate(category_count=Count('categoria_id__subcategoria_id'))
        
    #     subcatgory= SubCategory.objects.annotate(subcategory_count=Count('subcategoria_id'))
            
    #     marca=Marcas.objects.annotate(product_count=Count('marca_id'))

    #     return render(request,self.template_name,{"category":category,"subcategory":subcatgory,"marca":marca})
    



 