# apps/purchase/models.py
from django.db import models
from apps.core.models import BaseModel
from apps.supplier.models import Supplier


class PurchaseOrder(BaseModel, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')])

    def __str__(self):
        return f"Purchase Order from {self.supplier.user.email} - {self.status}"
