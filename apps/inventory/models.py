# apps/inventory/models.py
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.product.models import Product


class Inventory(BaseModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField()
    last_restocked_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set last_restocked_at to the current time if the inventory is being created
        if not self.pk:  # Check if the instance is being created
            self.last_restocked_at = timezone.now()
        super().save(*args, **kwargs)

    def is_low_stock(self):
        """Returns True if quantity is below threshold."""
        return self.quantity < self.low_stock_threshold

    def __str__(self):
        return f"Inventory for {self.product.name}"