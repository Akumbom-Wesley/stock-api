from rest_framework import serializers
from .models import Supplier
from apps.user.serializers import UserSerializer


class SupplierSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'user', 'contact_info', 'address']
        read_only_fields = ['id', 'user']

