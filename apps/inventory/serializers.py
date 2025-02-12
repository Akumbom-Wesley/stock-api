# apps/inventory/serializers.py
from rest_framework import serializers
from .models import Inventory
from apps.product.models import Product


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")  # Display product name

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'quantity', 'low_stock_threshold', 'last_restocked_at']
        read_only_fields = ['last_restocked_at']  # Prevent manual updates to last_restocked_at
