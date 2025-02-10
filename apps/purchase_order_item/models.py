# apps/purchase/models.py
from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product
from apps.purchase_order.models import PurchaseOrder


class PurchaseOrderItem(BaseModel, models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase

    def __str__(self):
        return f"Item in {self.purchase_order} - {self.product.name}"