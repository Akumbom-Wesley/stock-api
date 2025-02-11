# apps/category/views.py
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated


# Create Category
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


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
