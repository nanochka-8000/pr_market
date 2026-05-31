from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import CategoryForm, ProductForm


def products_view(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/products.html', {'products': products})


def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_view')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {'form': form, 'title': 'Add Category', 'button': 'Add category'})


def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_view', product_id=product.pk)
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Add Product', 'button': 'Add product'})

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categories})


def category_edit_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories_view')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/category_form.html', {
        'form': form,
        'title': 'Edit Category',
        'button': 'Edit Category',
    })


def category_delete_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('categories_view')

def product_edit_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_view', product_id=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'button': 'Edit product',
    })


def product_delete_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect('products_view')