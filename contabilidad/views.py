from django.shortcuts import render, redirect
from datetime import date

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
    # 🔹 Datos quemados (solo para probar)
    cuentas = [
        {"codigo": "1.1.1", "nombre": "Efectivo y Equivalentes", "descripcion": "Recursos de liquidez inmediata.", "tipo": "activo"},
        {"codigo": "2.1.1", "nombre": "Proveedores", "descripcion": "Deudas con proveedores locales.", "tipo": "pasivo"},
        {"codigo": "3.1.1", "nombre": "Capital Social", "descripcion": "Aportes de los socios.", "tipo": "capital"},
        {"codigo": "4.1.1", "nombre": "Ventas", "descripcion": "Ingresos por venta de productos.", "tipo": "ingresos"},
        {"codigo": "5.1.1", "nombre": "Gastos Administrativos", "descripcion": "Costos de operación general.", "tipo": "gastos"},
    ]

    # 🔹 Código real (descomentar cuando tengas la BD)
    # cuentas = Cuenta.objects.all()

    context = {
        'cuentas': cuentas
    }

    return render(request, 'contabilidad/catalogo_cuentas.html', context)
# -------------------------
# Nueva Transacción
# -------------------------
def nueva_transaccion(request):
    # Puedes pasar datos al template si es necesario, por ejemplo para activar el item del menú
    context = {
        'active_page': 'transacciones' # Esto ayuda a destacar "Transacciones" en el sidebar
    }
    return render(request, 'contabilidad/nueva_transaccion.html', context)



# -------------------------
# Estado Financiero
# -------------------------
def estado_financiero(request):
    # Renderiza el template de estados financieros
    return render(request, 'contabilidad/estado_financiero.html')


# -------------------------
# Libro Mayor
# -------------------------
def libro_mayor(request):
    
    # --- 1. OBTENER LA CUENTA SELECCIONADA DEL FILTRO ---
    selected_cuenta = request.GET.get('cuenta', None)

    # --- 2. OBTENER DATOS ---

    # =================================================================================
    # BLOQUE 1: DATOS QUEMADOS PARA PRUEBAS (BORRAR ESTE BLOQUE LUEGO)
    # =================================================================================
    datos_completos = [
        # Datos de Caja
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 15), 'numero': 'IV-001', 'descripcion': 'Venta de contado #1', 'debe': 1500.00, 'haber': 0.00, 'saldo': 1500.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 18), 'numero': 'EG-001', 'descripcion': 'Pago de servicios básicos', 'debe': 0.00, 'haber': 300.00, 'saldo': 1200.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        
        # Datos de Banco
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 16), 'numero': 'DEP-001', 'descripcion': 'Depósito inicial', 'debe': 50000.00, 'haber': 0.00, 'saldo': 50000.00},
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 20), 'numero': 'CH-001', 'descripcion': 'Pago a proveedor A (Cheque)', 'debe': 0.00, 'haber': 12000.00, 'saldo': 38000.00},
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 25), 'numero': 'TR-001', 'descripcion': 'Transferencia de cliente B', 'debe': 7500.00, 'haber': 0.00, 'saldo': 45500.00},

        # Datos de Proveedores
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 10), 'numero': 'FC-050', 'descripcion': 'Compra de materia prima', 'debe': 0.00, 'haber': 12000.00, 'saldo': -12000.00},
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 20), 'numero': 'CH-001', 'descripcion': 'Abono con cheque', 'debe': 12000.00, 'haber': 0.00, 'saldo': 0.00},
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 28), 'numero': 'FC-090', 'descripcion': 'Compra de insumos de oficina', 'debe': 0.00, 'haber': 4000.00, 'saldo': -4000.00},
    ]
    todas_las_cuentas = sorted(list(set(item['cuenta'] for item in datos_completos)))
    cuentas_a_mostrar = [item for item in datos_completos if item['cuenta'] == selected_cuenta] if selected_cuenta else []
    # =================================================================================
    # FIN DEL BLOQUE DE DATOS QUEMADOS
    # =================================================================================


    # =================================================================================
    # BLOQUE 2: CÓDIGO REAL DE BASE DE DATOS (DESCOMENTAR ESTE BLOQUE LUEGO)
    # ¡Ajusta los nombres del modelo ('MovimientoContable') y los campos ('cuenta', 'fecha', etc.)!
    # =================================================================================
    # # Obtiene la lista de nombres de cuentas únicos para el menú desplegable
    # todas_las_cuentas = MovimientoContable.objects.order_by('cuenta').values_list('cuenta', flat=True).distinct()

    # # Filtra los movimientos de la cuenta seleccionada
    # cuentas_a_mostrar = []
    # if selected_cuenta:
    #     queryset = MovimientoContable.objects.filter(cuenta=selected_cuenta).order_by('fecha', 'id')
    #     cuentas_a_mostrar = list(queryset.values('fecha', 'numero', 'descripcion', 'debe', 'haber', 'saldo'))
    # =================================================================================
    # FIN DEL BLOQUE DE BASE DE DATOS
    # =================================================================================
    

    # --- 3. CALCULAR TOTALES (solo de los datos filtrados) ---
    total_debe = sum(item.get('debe', 0) for item in cuentas_a_mostrar)
    total_haber = sum(item.get('haber', 0) for item in cuentas_a_mostrar)
    total_saldo = cuentas_a_mostrar[-1]['saldo'] if cuentas_a_mostrar else 0

    totales = {
        'total_debe': total_debe,
        'total_haber': total_haber,
        'total_saldo': total_saldo,
    }

    # --- 4. CONSTRUIR EL CONTEXTO Y RENDERIZAR LA PLANTILLA ---
    context = {
        'cuentas': cuentas_a_mostrar,
        'totales': totales,
        'todas_las_cuentas': todas_las_cuentas,
        'selected_cuenta': selected_cuenta,
    }
    
    return render(request, 'contabilidad/libro_mayor.html', context)

# ------------------------------------
# Vista para Imprimir Libro Mayor
# (Esta vista también necesita ser actualizada cuando cambies a la base de datos)
# ------------------------------------
def libro_mayor_imprimir(request):
    selected_cuenta = request.GET.get('cuenta', None)
    
    # Reutiliza la misma lógica de la vista principal para obtener los datos
    # (Aquí también deberás reemplazar los datos quemados por la consulta a la BD)
    datos_completos = [
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 15), 'numero': 'IV-001', 'descripcion': 'Venta de contado #1', 'debe': 1500.00, 'haber': 0.00, 'saldo': 1500.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 18), 'numero': 'EG-001', 'descripcion': 'Pago de servicios básicos', 'debe': 0.00, 'haber': 300.00, 'saldo': 1200.00},
        {'cuenta': 'Caja', 'fecha': date(2025, 1, 22), 'numero': 'IV-002', 'descripcion': 'Venta de contado #2', 'debe': 2500.00, 'haber': 0.00, 'saldo': 3700.00},
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 16), 'numero': 'DEP-001', 'descripcion': 'Depósito inicial', 'debe': 50000.00, 'haber': 0.00, 'saldo': 50000.00},
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 20), 'numero': 'CH-001', 'descripcion': 'Pago a proveedor A (Cheque)', 'debe': 0.00, 'haber': 12000.00, 'saldo': 38000.00},
        {'cuenta': 'Banco', 'fecha': date(2025, 1, 25), 'numero': 'TR-001', 'descripcion': 'Transferencia de cliente B', 'debe': 7500.00, 'haber': 0.00, 'saldo': 45500.00},
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 10), 'numero': 'FC-050', 'descripcion': 'Compra de materia prima', 'debe': 0.00, 'haber': 12000.00, 'saldo': -12000.00},
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 20), 'numero': 'CH-001', 'descripcion': 'Abono con cheque', 'debe': 12000.00, 'haber': 0.00, 'saldo': 0.00},
        {'cuenta': 'Proveedores', 'fecha': date(2025, 1, 28), 'numero': 'FC-090', 'descripcion': 'Compra de insumos de oficina', 'debe': 0.00, 'haber': 4000.00, 'saldo': -4000.00},
    ]

    cuentas_a_mostrar = [item for item in datos_completos if item['cuenta'] == selected_cuenta] if selected_cuenta else []

    total_debe = sum(item.get('debe', 0) for item in cuentas_a_mostrar)
    total_haber = sum(item.get('haber', 0) for item in cuentas_a_mostrar)
    total_saldo = cuentas_a_mostrar[-1]['saldo'] if cuentas_a_mostrar else 0

    totales = {'total_debe': total_debe, 'total_haber': total_haber, 'total_saldo': total_saldo}

    context = {'cuentas': cuentas_a_mostrar, 'totales': totales, 'selected_cuenta': selected_cuenta}
    
    return render(request, 'contabilidad/libro_mayor_imprimir.html', context)