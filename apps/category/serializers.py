# apps/category/serializers.py
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
