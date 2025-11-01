

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """Vista de login unificada"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirigir según el rol del usuario
            if user.rol == user.ROL_CONTADOR:
                return redirect('contabilidad:panel_principal')
            elif user.rol == user.ROL_AUDITOR:
                return redirect('contabilidad:panel_principal')
            else:
                return redirect('contabilidad:panel_principal')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'usuarios/login.html')

def dashboard_view(request):
    """Dashboard para usuarios logueados"""
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    return render(request, 'usuarios/index.html')

def logout_view(request):
    """Cerrar sesión"""
    logout(request) # <--- Cierra la sesión activa de Django
    # Redirige al login después de cerrar la sesión
    return redirect('usuarios:login')