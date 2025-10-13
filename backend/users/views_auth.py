from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.rol in ["orientador", "institucion"]:
            msg = (
                "Registro recibido correctamente. "
                "Un administrador revisará tus documentos antes de activar tu cuenta."
            )
        else:
            msg = "Registro exitoso. Ya puedes iniciar sesión."

        return Response(
            {
                "message": msg,
                "rol": user.rol,
                "email": user.email,
                "activo": user.activo,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(generics.GenericAPIView):
    """
    Login principal (email + contraseña)
    ✅ Verifica credenciales
    ✅ Bloquea usuarios inactivos
    ✅ Devuelve tokens con rol, nombre, activo, etc.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Faltan credenciales."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 🚫 Bloquear acceso a usuarios inactivos
        if not getattr(user, "activo", True):
            return Response(
                {"detail": "Tu cuenta está inactiva. Un administrador debe activarla antes de ingresar."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Usuario activo → generar tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Agregar campos personalizados al token
        for t in (refresh, access_token):
            t["email"] = user.email
            t["nombre"] = getattr(user, "nombre", "")
            t["apellido"] = getattr(user, "apellido", "")
            t["rol"] = getattr(user, "rol", "estudiante")
            t["activo"] = getattr(user, "activo", True)

        # 🧩 Respuesta para frontend
        return Response(
            {
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(refresh),
                },
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "nombre": getattr(user, "nombre", ""),
                    "apellido": getattr(user, "apellido", ""),
                    "rol": getattr(user, "rol", "estudiante"),
                    "activo": getattr(user, "activo", True),
                },
            },
            status=status.HTTP_200_OK,
        )

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data.get("refresh")
            token_obj = RefreshToken(token)
            token_obj.blacklist()
            return Response({"message": "Sesión cerrada correctamente."})
        except Exception:
            return Response(
                {"error": "Token inválido o ya expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
