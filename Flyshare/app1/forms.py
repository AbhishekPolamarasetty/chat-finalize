# app1/forms.py
from django import forms
from app1.models import PostModel

class PostModelFrom(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = '__all__'

