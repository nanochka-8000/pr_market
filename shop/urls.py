from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_view'),
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/add', views.ProductCreateView.as_view(), name='product_add_view'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product_view'),
    path('products/<int:product_id>/edit', views.ProductUpdateView.as_view(), name='product_edit_view'),
    path('products/<int:product_id>/delete', views.ProductDeleteView.as_view(), name='product_delete_view'),
    path('products/<slug:category_slug>/', views.CategoryProductListView.as_view(), name='category_products_view'),

    path('categories/', views.categories_view, name='categories_view'),
    path('categories/add', views.category_add_view, name='category_add_view'),
    path('categories/<int:category_id>/edit', views.category_edit_view, name='category_edit_view'),
    path('categories/<int:category_id>/delete', views.category_delete_view, name='category_delete_view'),

    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='cart_add'),
    path('cart/remove/<int:pk>/', views.RemoveFromCartView.as_view(), name='cart_remove'),
    path('cart/decrease/<int:pk>/', views.DecreaseCartItemView.as_view(), name='cart_decrease'),
]