from django import forms
from .models import Category, Product
from .models import Order


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

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError('Остаток не может быть меньше 0.')
        return stock

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

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


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }
        labels = {'name': '', 'address': '', 'phone': ''}