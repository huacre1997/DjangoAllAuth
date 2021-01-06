from django.db.models import Count
from django.apps import apps 
from cart.cart import Cart
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def marcas(request):

    from products.models import Marcas
    from cart.models import Cart
    marca=Marcas.objects.only("id","name","slug").annotate(marca_count=Count('marca_id'))

    if request.user:
        amount=Cart.objects.amount(request.user)
    else:
        amount=request.session.get("cart")


    return {'marca':marca,"amount":amount}


def category(request):
    from products.models import Category,Product
    category=Category.objects.add_related_count(
                Category.objects.all(),
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

                
    
    return {"category":category}