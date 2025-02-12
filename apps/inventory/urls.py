# apps/inventory/urls.py
from django.urls import path
from .views import create_inventory, InventoryListView, InventoryRetrieveView, update_inventory, delete_inventory

urlpatterns = [
    path('create/', create_inventory, name='create-inventory'),
    path('list/', InventoryListView.as_view(), name='inventory-list'),
    path('<int:pk>/', InventoryRetrieveView.as_view(), name='inventory-detail'),
    path('update/<int:id>/', update_inventory, name='inventory-update'),
    path('delete/<int:id>/', delete_inventory, name='inventory-delete'),
]
