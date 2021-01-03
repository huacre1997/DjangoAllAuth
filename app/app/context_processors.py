from django.db.models import Count
from django.apps import apps 
from cart.cart import Cart
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def marcas(request):

    from products.models import Marcas
    marca=Marcas.objects.only("id","name","slug").annotate(marca_count=Count('marca_id'))
    print()

    return {'marca':marca,"cart":Cart(request),"cartdrop":request.session.get("cart")}


def category(request):
    from products.models import Category,Product
    category=Category.objects.add_related_count(
                Category.objects.all(),
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

                
    
    return {"category":category}