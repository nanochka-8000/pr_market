from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CategoryForm, ProductForm, ProductSearchForm
from .models import Category, Product
from django.views import View

from .models import CartItem
from django.db import transaction

from .forms import OrderForm
from .models import Order, OrderItem

class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        qs = Product.objects.filter(stock__gte=1).select_related('category')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs.order_by('category__name', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductSearchForm(self.request.GET or None)
        ctx['categories'] = Category.objects.all().order_by('name')
        ctx['title'] = 'All products'
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class CategoryProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        qs = Product.objects.filter(category=self.category, stock__gte=1).select_related('category')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductSearchForm(self.request.GET or None)
        ctx['categories'] = Category.objects.all().order_by('name')
        ctx['current_category'] = self.category
        ctx['title'] = self.category.name
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Product'
        ctx['button'] = 'Add product'
        return ctx

    def get_success_url(self):
        return reverse_lazy('product_view', kwargs={'product_id': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Product'
        ctx['button'] = 'Edit product'
        return ctx

    def get_success_url(self):
        return reverse_lazy('product_view', kwargs={'product_id': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('products_view')


def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categories})


def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_view')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {
        'form': form, 'title': 'Add Category', 'button': 'Add category'
    })


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
        'form': form, 'title': 'Edit Category', 'button': 'Edit Category',
    })


def category_delete_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('categories_view')



class AddToCartView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product)

        if created:
            if product.stock < 1:
                cart_item.delete()
            else:
                cart_item.quantity = 1
                cart_item.save()
        else:
            if cart_item.quantity + 1 <= product.stock:
                cart_item.quantity += 1
                cart_item.save()

        return self._redirect_back(request, product)

    def _redirect_back(self, request, product):
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('products_view')


class CartView(ListView):
    model = CartItem
    template_name = 'shop/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.select_related('product').order_by('product__name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = ctx['cart_items']
        ctx['total'] = sum(item.total for item in items)
        ctx['order_form'] = OrderForm()
        return ctx


class RemoveFromCartView(View):

    def get(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return redirect('cart_view')


class DecreaseCartItemView(View):

    def get(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart_view')


class CreateOrderView(View):

    def post(self, request):
        form = OrderForm(request.POST)
        cart_items = CartItem.objects.select_related('product').all()

        if not cart_items.exists():
            return redirect('cart_view')

        if form.is_valid():
            with transaction.atomic():
                order = form.save()
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                    )
                cart_items.delete()
            return redirect('order_success', pk=order.pk)

        total = sum(item.total for item in cart_items)
        return render(request, 'shop/cart.html', {
            'cart_items': cart_items,
            'total': total,
            'order_form': form,
        })


class OrderSuccessView(DetailView):
    model = Order
    template_name = 'shop/order_success.html'
    context_object_name = 'order'