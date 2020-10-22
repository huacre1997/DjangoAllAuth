from django.db import models
from base.models import BaseModel
from crum import get_current_user

class Category(BaseModel):
    name = models.CharField(verbose_name="Nombre Categoría",max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
class SubCategory(BaseModel):

    category=models.ForeignKey(Category, verbose_name="Categoría", on_delete=models.CASCADE,related_name="categoria_id")
    name = models.CharField(verbose_name="Nombre Subcategoría",max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'SubCategoria'
        verbose_name_plural = 'SubCategorias'
        