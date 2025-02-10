# apps/inventory/models.py
from django.db import models

from apps.category.models import Category
from apps.core.models import BaseModel


class Product(BaseModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name