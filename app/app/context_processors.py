from django.db.models import Count
from django.apps import apps 
from cart.cart import Cart 
from products.models import Marcas
from cart.models import Cart as CartModel,CartItem
from django.conf import settings 

# subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def marcas(request):
  
    marca=Marcas.objects.only("id","name","slug").annotate(marca_count=Count('marca_id'))

    if  request.user.is_authenticated:
        data=Cart(request)
        p,status=CartModel.objects.only("quantity").get_or_create(user_id=request.user.id)
        print(data.cart)
        data.clear()

        return {'marca':marca,"amount":p.quantity}
    else:
        return {'marca':marca,"cart":Cart(request)}



   


def category(request):
    from products.models import Category,Product
    category=Category.objects.add_related_count(
                Category.objects.all(),
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

                
    
    return {"category":category}