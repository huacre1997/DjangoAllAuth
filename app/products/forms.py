from django import forms
from .models import *

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields="__all__"
    def save(self, commit=True):
        instance = super(SubCategoryForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    def clean_slug(self):
        print(self.cleaned_data["slug"])
        return self.cleaned_data["slug"]