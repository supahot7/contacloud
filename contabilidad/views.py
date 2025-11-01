from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cuenta
from usuarios.views import login_view

# -------------------------
# Panel principal (protegido)
# -------------------------
@login_required(login_url='usuarios:login')
def panel_principal(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'contabilidad/index.html', context)

# -------------------------
# Catálogo de cuentas (protegido)
# -------------------------
@login_required(login_url='/login/')
def catalogo_cuentas(request):
    # Obtener todas las cuentas de la base de datos
    cuentas = Cuenta.objects.all().order_by('codigo')
    
    # Pasar las cuentas al template
    context = {
        'cuentas': cuentas
    }
    return render(request, 'contabilidad/catalogo_cuentas.html', context)

