from django.shortcuts import render, redirect

# -------------------------
# Login (simulado)
# -------------------------
def login_view(request):
    if request.method == 'POST':
        # Aquí podrías agregar lógica real de autenticación
        print("Formulario de login enviado!")
        return render(request, 'login.html', {'message': 'Login exitoso (simulado)'})
    
    return render(request, 'login.html')


# -------------------------
# Panel principal
# -------------------------

def panel_principal(request):
    return render(request, 'contabilidad/index.html')



# -------------------------
# Catálogo de cuentas
# -------------------------
def catalogo_cuentas(request):
    # Se recomienda usar snake_case en el nombre del template
    return render(request, 'contabilidad/catalogoCuentas.html')

# -------------------------
# Estados Financieros
# -------------------------

def estados_financieros(request):
    return render(request, 'contabilidad/estadosFinancieros.html')

# -------------------------
# Balance General
# -------------------------

def balance_general(request):
    return render(request, 'contabilidad/balanceGeneral.html')

# -------------------------
# Estado de Resultados
# -------------------------

def estado_resultados(request):
    return render(request, 'contabilidad/estadoResultados.html')

# -------------------------
# Estado de Capital
# -------------------------

def estado_capital(request):
    return render(request, 'contabilidad/estadoCapital.html')

# -------------------------
# Mano de Obra
# -------------------------

def mano_obra(request):
    return render(request, 'contabilidad/manoObra.html')

# -------------------------
# Inventario de Licencias
# -------------------------

def inventario_licencias(request):
    return render(request, 'contabilidad/inventarioLicencias.html')


# -------------------------
# Inventario de Licencias
# -------------------------

def planilla(request):
    return render(request, 'contabilidad/planilla.html')