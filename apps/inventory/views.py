# apps/inventory/views.py
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now

from .models import Inventory
from .serializers import InventorySerializer
from ..product.models import Product


# Create a new inventory
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_inventory(request):
    """
    Create an inventory item for a specific product. Only the supplier of the product can create inventory for it.
    """
    product_id = request.data.get("product")
    quantity = request.data.get("quantity")
    low_stock_threshold = request.data.get("low_stock_threshold")

    # Check if the product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is the supplier (owner) of the product
    if product.owner.user != request.user:
        return Response({"error": "You are not authorized to create inventory for this product"}, status=status.HTTP_403_FORBIDDEN)

    # Create the inventory item data
    inventory_data = {
        "product": product_id,
        "quantity": quantity,
        "low_stock_threshold": low_stock_threshold,
    }

    # Validate and save inventory
    serializer = InventorySerializer(data=inventory_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryListView(generics.ListAPIView):
    """List all inventory items."""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


# Retrieve a single inventory item
class InventoryRetrieveView(generics.RetrieveAPIView):
    """Retrieve details of a specific inventory item."""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


#  Update inventory (Manual Adjustments)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_inventory(request, id):
    """
    Update the inventory item. Restocking will update the last_restocked_at field only if the quantity is updated.
    """
    try:
        inventory = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the logged-in user is the owner of the product
    if inventory.product.owner.user != request.user:
        return Response({"error": "You are not authorized to update this inventory"}, status=status.HTTP_403_FORBIDDEN)

    # Create a serializer instance with the partial update
    serializer = InventorySerializer(inventory, data=request.data, partial=True)

    if serializer.is_valid():
        # Check if 'quantity' is among the fields that are being updated
        if 'quantity' in serializer.validated_data:
            inventory.last_restocked_at = timezone.now()  # Update restock time when quantity changes

        # Save the updated inventory
        serializer.save()

        # Return updated data
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Inventory
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_inventory(request, id):
    """
    Delete an inventory item for a specific product. Only the supplier of the product can delete the inventory.
    """
    try:
        inventory = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is the supplier (owner) of the product
    if inventory.product.owner.user != request.user:
        return Response({"error": "You are not authorized to delete this product's inventory"}, status=status.HTTP_403_FORBIDDEN)

    # Proceed with deleting the inventory
    inventory.delete()
    return Response({"message": "Inventory item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)