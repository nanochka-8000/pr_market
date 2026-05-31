from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 5}),
        }
        labels = {'name': '', 'description': ''}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Title'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'step': '0.01'}),
            'image': forms.URLInput(attrs={'placeholder': 'Image url'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 5}),
        }
        labels = {'name': '', 'price': '', 'image': '', 'category': '', 'description': ''}