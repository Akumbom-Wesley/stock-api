from rest_framework import serializers
from .models import Product
from apps.category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.ReadOnlyField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # Change this line
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_price', 'sku', 'category', 'owner']

    def create(self, validated_data):
        """
        Ensure the product is linked to an existing category.
        """
        category = validated_data.get("category")
        if not category:
            raise serializers.ValidationError({"category": "Category is required."})

        return Product.objects.create(**validated_data)