from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
import requests
from urllib.parse import urlencode
from django.conf import settings


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope=openid email profile https://www.googleapis.com/auth/calendar.events"
            f"&access_type=offline&prompt=consent"
        )
        return JsonResponse({"auth_url": google_auth_url})

class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

        # Log temporal para depurar
        print("🔹 Using redirect URI:", settings.GOOGLE_REDIRECT_URI)
        print("🔹 Client ID:", settings.GOOGLE_CLIENT_ID[:10], "...")

        # Intercambio del código por tokens de Google
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        try:
            r = requests.post(token_url, data=data)
            if r.status_code != 200:
                print("❌ Token exchange error:", r.text)
                return Response(
                    {"error": "Token exchange failed", "details": r.text},
                    status=r.status_code,
                )
        except requests.exceptions.RequestException as e:
            print("❌ Request exception:", e)
            return Response({"error": "Request exception", "details": str(e)}, status=500)

        tokens = r.json()
        google_access_token = tokens.get("access_token")
        google_refresh_token = tokens.get("refresh_token")

        # Obtener info del usuario
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {google_access_token}"}
        r = requests.get(userinfo_url, headers=headers)
        if r.status_code != 200:
            print("❌ User info error:", r.text)
            return Response({"error": "Failed to get user info"}, status=r.status_code)

        userinfo = r.json()
        email = userinfo.get("email")
        nombre = userinfo.get("given_name", "")
        apellido = userinfo.get("family_name", "")

        user, created = Usuario.objects.get_or_create(
            email=email,
            defaults={"nombre": nombre, "apellido": apellido, "rol": "estudiante"},
        )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        access["email"] = user.email
        access["nombre"] = user.nombre
        access["apellido"] = user.apellido
        access["rol"] = user.rol
        access["id"] = str(user.id)
        access["activo"] = user.activo

        frontend_url = f"{settings.FRONTEND_URL.rstrip('/')}/google/callback"
        params = {
            "access": str(access),
            "refresh": str(refresh),
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "rol": user.rol,
            "google_access_token": google_access_token,
            "google_refresh_token": google_refresh_token,
        }
        redirect_url = f"{frontend_url}?{urlencode(params)}"
        print("✅ Redirecting to frontend:", redirect_url)
        return redirect(redirect_url)
