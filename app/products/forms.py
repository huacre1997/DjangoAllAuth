from django import forms

class RatingForm(forms.Form):
    author = forms.CharField(max_length=100)
    comment = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)