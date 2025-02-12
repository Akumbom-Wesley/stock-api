# apps/category/views.py
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated

from ..supplier.models import Supplier


# Create Category
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_category(request):
    """
    Create a new category and assign the owner to the logged-in user's supplier account.
    """
    try:
        # Get the Supplier instance associated with the logged-in user
        supplier = Supplier.objects.get(user=request.user)

        data = request.data.copy()
        data['supplier'] = supplier.id  # Set the owner to the supplier's ID

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(supplier=supplier)  # Pass the supplier instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Supplier.DoesNotExist:
        return Response(
            {"error": "You must be registered as a supplier to create categories"},
            status=status.HTTP_403_FORBIDDEN
        )


# List Categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Retrieve a specific Category
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Update Category
class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        """Allow partial updates (PATCH behavior)."""
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


# Delete Category
@api_view(['DELETE'])
@permission_classes(IsAuthenticated)
def delete_category(request, id):

    """Delete a category."""
    try:
        category = Category.objects.get(id=id)
        # Ensure no products are associated with this category before deleting it.
        if category.product_set.exists():
            return Response({"error": "Category has associated products, cannot delete."},
                            status=status.HTTP_400_BAD_REQUEST)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
