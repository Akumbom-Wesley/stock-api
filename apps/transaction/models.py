# apps/transaction/models.py
from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product


class Transaction(BaseModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=[('Sale', 'Sale'), ('Restock', 'Restock'), ('Adjustment', 'Adjustment')])
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.transaction_type} for {self.product.name}"
