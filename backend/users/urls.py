from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet
from .auth import login_view, register_view, logout_view
from .views_google import GoogleLoginView, GoogleCallbackView
from .views_jwt import CustomTokenObtainPairView

# 🔹 Configuración del router para CRUD de usuarios
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    # -------------------------------
    # 🔐 Autenticación por email/password
    # -------------------------------
    path("auth/register/", register_view, name="register"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),

    # -------------------------------
    # 🔑 JWT personalizado
    # -------------------------------
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # -------------------------------
    # 🌐 Autenticación con Google OAuth
    # -------------------------------
    path("auth/google/login/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/google/callback/", GoogleCallbackView.as_view(), name="google-callback"),

    # -------------------------------
    # 👤 CRUD de usuarios
    # -------------------------------
    path("", include(router.urls)),
]
