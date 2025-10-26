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






