# apps/category/urls.py
from django.urls import path
from .views import create_category, CategoryListView, CategoryDetailView, CategoryUpdateView, delete_category

urlpatterns = [
    path('list', CategoryListView.as_view(), name='category-list'),
    path('create/', create_category, name='category-create'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('delete/<int:pk>/', delete_category, name='category-delete'),
]
