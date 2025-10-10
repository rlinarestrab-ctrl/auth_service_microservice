from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Genera un token JWT con información personalizada del usuario.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔹 Agregamos información adicional al payload
        token["email"] = user.email
        token["nombre"] = user.nombre
        token["apellido"] = user.apellido
        token["rol"] = user.rol
        token["id"] = str(user.id)
        token["activo"] = user.activo

        return token
