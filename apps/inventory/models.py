# apps/inventory/models.py
from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product


class Inventory(BaseModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField()
    last_restocked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Inventory for {self.product.name}"