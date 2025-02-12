# apps/product/urls.py
from django.urls import path
from .views import (
    create_product, ProductListView, ProductRetrieveView,
    update_product, delete_product
)

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', create_product, name='product-create'),
    path('<int:pk>/', ProductRetrieveView.as_view(), name='product-detail'),
    path('update/<int:id>/', update_product, name='product-update'),
    path('delete/<int:id>/', delete_product, name='product-delete'),
]
