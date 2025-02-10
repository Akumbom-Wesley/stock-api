# apps/inventory/models.py
from django.db import models
from apps.core.models import BaseModel


class Category(BaseModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name