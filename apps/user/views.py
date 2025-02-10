from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """Handles user registration"""
    permission_classes = [permissions.AllowAny]  # Allows anyone to register
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    """Custom login view that uses email and password and returns only the tokens"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Custom POST method to authenticate using email and password
        and return only the JWT tokens (access and refresh).
        """
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password are required")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("No active account found with the given credentials")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        # Call the TokenObtainPairView to generate tokens
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that only returns tokens"""
    serializer_class = CustomTokenObtainPairSerializer
