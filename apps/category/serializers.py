# apps/category/serializers.py
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'supplier']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
