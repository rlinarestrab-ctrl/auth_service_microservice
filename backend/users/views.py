from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Usuario
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdmin, IsSelfOrAdmin


# -----------------------------
# 👥 CRUD de usuarios
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuarios (solo admin puede listar, crear y borrar).
    Permite búsqueda por nombre, apellido o email.
    """
    queryset = Usuario.objects.all().order_by("-fecha_registro")
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ["list", "create", "destroy"]:
            return [IsAdmin()]
        if self.action in ["retrieve", "update", "partial_update"]:
            return [IsSelfOrAdmin()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        qs = self.get_queryset()
        if q:
            qs = qs.filter(
                Q(email__icontains=q) |
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q)
            )
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)


# -----------------------------
# 🔐 Login JWT extendido (oficial)
# -----------------------------
class LoginJWTView(TokenObtainPairView):
    """
    Retorna access y refresh tokens con campos personalizados (rol, nombre, etc.)
    """
    serializer_class = CustomTokenObtainPairSerializer


# -----------------------------
# ⚙️ (Opcional) Login manual simple
# -----------------------------
class LoginView(APIView):
    """
    Vista alternativa de login clásico (email + password),
    mantiene compatibilidad si ya usas esta ruta en el frontend.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Faltan credenciales"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generar tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # ✅ Agregar información personalizada al token (igual que en CustomTokenObtainPairSerializer)
        access_token["email"] = user.email
        access_token["nombre"] = user.nombre
        access_token["apellido"] = user.apellido
        access_token["rol"] = user.rol

        return Response({
            "tokens": {
                "access": str(access_token),
                "refresh": str(refresh),
            },
            "user": {
                "id": str(user.id),
                "email": user.email,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "rol": user.rol,
            }
        }, status=status.HTTP_200_OK)
