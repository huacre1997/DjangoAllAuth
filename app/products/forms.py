from django.forms import ModelForm
from .models import Comment
class RatingForm(ModelForm):
    class Meta:
        model=Comment
        fields=["author","comment","rate"]
  