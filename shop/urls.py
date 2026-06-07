from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_view, name='products_view'),
    path('products/', views.products_view, name='products_list'),
    path('products/add', views.product_add_view, name='product_add_view'),
    path('products/<int:product_id>/', views.product_view, name='product_view'),
    path('products/<int:product_id>/edit', views.product_edit_view, name='product_edit_view'),
    path('products/<int:product_id>/delete', views.product_delete_view, name='product_delete_view'),
    path('products/<slug:category_slug>/', views.category_products_view, name='category_products_view'),
    path('categories/', views.categories_view, name='categories_view'),
    path('categories/add', views.category_add_view, name='category_add_view'),
    path('categories/<int:category_id>/edit', views.category_edit_view, name='category_edit_view'),
    path('categories/<int:category_id>/delete', views.category_delete_view, name='category_delete_view'),
]