from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UsuarioSerializer

# Create your views here.
class UserStatusView(APIView):
    # La clave es esta línea: Si no hay un token válido, se deniega el acceso.
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # 'request.user' ya fue autenticado por JWT y IsAuthenticated.
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# VISTAS HTML (Servidor Web) ---------------------------------------------------

def login_view(request):
    """ Sirve el template de login.html. """
    # Asume que el template está en 'usuarios/templates/usuarios/login.html'
    return render(request, 'usuarios/login.html') 

def dashboard_view(request):
    """ Sirve el template principal de la aplicación (Dashboard). """
    # Asume que el template está en 'usuarios/templates/usuarios/dashboard.html'
    return render(request, 'usuarios/index.html') 

# VISTAS API (DRF) ------------------------------------------------------------

class UserStatusView(APIView):
    """
    API protegida para verificar el estado de un token JWT y obtener datos de usuario.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user es una instancia de tu modelo Usuario (con el campo rol)
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)