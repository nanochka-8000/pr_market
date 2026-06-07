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
    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'})
    )
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'})
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'stock', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Image url'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 5}),
        }
        labels = {'name': '', 'image': '', 'category': '', 'description': ''}

class ProductSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию...',
        })
    )