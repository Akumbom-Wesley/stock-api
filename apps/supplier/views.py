# apps/accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Supplier
from .serializers import SupplierSerializer


User = get_user_model()


class SupplierCreateView(generics.CreateAPIView):
    """Create a new supplier account"""
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure supplier is linked to the authenticated user"""
        serializer.save(user=self.request.user)


class SupplierListView(generics.ListAPIView):
    """List all suppliers"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplierProfileView(generics.RetrieveAPIView):
    """Retrieve, update, or delete a supplier"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limit suppliers to the authenticated user's supplier profile"""
        return Supplier.objects.filter(user=self.request.user)


@api_view(['PUT'])
def supplier_update_view(request):
    """Update the supplier profile of the authenticated user."""
    try:
        # Retrieve the supplier profile for the authenticated user
        supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        return Response(
            {"error": "Supplier profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if the logged-in user is the one trying to update their profile
    if supplier.user != request.user:
        raise PermissionDenied("You do not have permission to update this profile.")

    # Use the SupplierSerializer to validate and update the supplier
    serializer = SupplierSerializer(supplier, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def supplier_delete_view(request):
    """Delete the authenticated user's supplier profile"""
    try:
        # Get the supplier profile related to the authenticated user
        supplier = Supplier.objects.get(user=request.user)

        # Check if the authenticated user matches the user of the supplier
        if supplier.user != request.user:
            return Response(
                {"error": "You are not authorized to delete this supplier profile."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Delete the supplier profile
        supplier.delete()

        return Response(
            {"message": "Supplier profile deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    except Supplier.DoesNotExist:
        return Response(
            {"error": "Supplier profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )


class SupplierDeleteAllView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(
            {"message": "All suppliers have been deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )