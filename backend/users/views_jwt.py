from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_jwt import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para emitir tokens JWT con datos del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer
