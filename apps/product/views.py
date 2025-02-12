# apps/product/views.py
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes

from .models import Product
from .serializers import ProductSerializer
from ..supplier.models import Supplier


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_product(request):
    """
    Create a new product and assign the owner to the logged-in user's supplier account.
    """
    try:
        # Get the Supplier instance associated with the logged-in user
        supplier = Supplier.objects.get(user=request.user)

        data = request.data.copy()
        data['owner'] = supplier.id  # Set the owner to the supplier's ID

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=supplier)  # Pass the supplier instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Supplier.DoesNotExist:
        return Response(
            {"error": "You must be registered as a supplier to create products"},
            status=status.HTTP_403_FORBIDDEN
        )


class ProductListView(generics.ListAPIView):
    """List all products (publicly accessible)."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductRetrieveView(generics.RetrieveAPIView):
    """Retrieve a single product by ID."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_product(request, id):
    """
    Update a product. Only the owner (Supplier) of the product can update it.
    """
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if product.owner.user != request.user:  # Make sure it checks Supplier's User
        return Response({"error": "You are not authorized to update this product"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_product(request, id):
    """
    Delete a product. Only the owner (Supplier) of the product can delete it.
    """
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if product.owner.user != request.user:  # Ensure correct ownership check
        return Response({"error": "You are not authorized to delete this product"}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)