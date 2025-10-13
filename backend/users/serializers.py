import re
import dns.resolver
import os
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Usuario, PerfilEstudiante, PerfilOrientador
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 🧩 1. Serializer general de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = [
            "id", "email", "password", "nombre", "apellido",
            "fecha_nacimiento", "telefono", "rol",
            "fecha_registro", "ultimo_login", "activo"
        ]
        read_only_fields = ["fecha_registro", "ultimo_login", "id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# 🔐 2. Serializer de Login clásico
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        user.ultimo_login = timezone.now()
        user.save(update_fields=["ultimo_login"])
        attrs["user"] = user
        return attrs


# 🚀 3. Serializer para JWT extendido
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extiende el token JWT para incluir más datos del usuario."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["nombre"] = user.nombre
        token["apellido"] = user.apellido
        token["rol"] = user.rol
        return token


# 🚫 Dominios temporales conocidos
DISPOSABLE_DOMAINS = {
    "mailinator.com", "yopmail.com", "guerrillamail.com", "10minutemail.com",
    "tempmail.com", "fakeinbox.com", "sharklasers.com", "trashmail.com",
    "maildrop.cc", "getnada.com", "dispostable.com", "mailnesia.com",
}

# ⚙️ Variable de entorno: valida MX solo en producción
VALIDAR_DOMINIO_EMAIL = os.getenv("VALIDAR_DOMINIO_EMAIL", "0") == "1"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["nombre", "apellido", "email", "password", "rol", "telefono"]

    # --- 🧠 Validación avanzada del email ---
    def validate_email(self, value):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError("El formato del correo no es válido.")

        dominio = value.split("@")[1].lower()

        # ❌ Bloquear dominios temporales
        if dominio in DISPOSABLE_DOMAINS:
            raise serializers.ValidationError(
                "No se permiten correos temporales o desechables."
            )

        # ✅ Validar dominio DNS solo si está activado
        if VALIDAR_DOMINIO_EMAIL:
            try:
                dns.resolver.resolve(dominio, "MX")
            except Exception:
                raise serializers.ValidationError(
                    f"El dominio '{dominio}' no parece tener un servidor de correo configurado."
                )

        # 🔁 Evitar duplicados
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")

        return value

    # --- 🔐 Crear usuario y su perfil ---
    def create(self, validated_data):
        password = validated_data.pop("password")
        rol = validated_data.get("rol", "estudiante")
        user = Usuario(**validated_data)
        user.set_password(password)

        # 🧱 Si requiere aprobación admin (orientador o institución)
        if rol in ["orientador", "institucion"]:
            user.activo = False

        # ✅ Se considera el email validado tras pasar la verificación
        user.save()

        # Crear perfiles según rol
        if rol == "estudiante":
            PerfilEstudiante.objects.create(usuario=user)
        elif rol == "orientador":
            PerfilOrientador.objects.create(usuario=user)

        return user