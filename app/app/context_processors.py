from django.db.models import Count
        # 
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def marcas(request):
    from products.models import Marcas
    marca=Marcas.objects.values("id","name","slug").annotate(marca_count=Count('marca_id'))
    return {'marca':marca}


def category(request):
    from products.models import Category
    category=Category.objects.all()
    return {"category":category}