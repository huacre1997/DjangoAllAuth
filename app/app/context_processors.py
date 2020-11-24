from django.db.models import Count
        # 
        # subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))   
def marcas(request):
    from products.models import Marcas
    return {'marca':Marcas.objects.values("id","name","slug").annotate(brand_count=Count('marca_id'))}


def category(request):
    from products.models import Category,SubCategory
    subcategory=SubCategory.objects.select_related("category").values("id","name","category").annotate(subcategory_count=Count('subcategoria_id'))
    return {"category":Category.objects.values("id","name","slug"),"subcategory":subcategory}