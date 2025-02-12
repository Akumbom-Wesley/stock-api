# apps/inventory/models.py
from django.db import models
from apps.core.models import BaseModel
from apps.supplier.models import Supplier


class Category(BaseModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name