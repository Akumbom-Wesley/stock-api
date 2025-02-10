# apps/accounts/models.py
from django.db import models
from apps.user.models import User
from apps.core.models import BaseModel


class Supplier(BaseModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.user.email
