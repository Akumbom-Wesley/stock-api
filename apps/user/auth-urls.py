from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_views import (
    RegisterView,
    CustomTokenObtainPairView,
    LoginView,
    ChangePasswordView,
    logout_view
)
from .views import UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("logout/", logout_view, name="logout"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]