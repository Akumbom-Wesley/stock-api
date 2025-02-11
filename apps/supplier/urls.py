# apps/accounts/urls.py
from django.urls import path
from .views import (
    SupplierCreateView,
    SupplierListView,
    SupplierProfileView,
    supplier_update_view,
    supplier_delete_view
)

urlpatterns = [
    path('list/', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/', SupplierProfileView.as_view(), name='supplier-detail'),
    path('delete/', supplier_delete_view, name='supplier-delete'),
    path('update/', supplier_update_view, name='supplier-delete'),
]
