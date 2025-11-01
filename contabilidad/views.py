from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from decimal import Decimal
from .models import Cuenta, Asiento, Partida
from django.utils import timezone

# -------------------------
# VISTA PRINCIPAL
# -------------------------
@login_required(login_url='/login/')
def panel_principal(request):
    """Panel principal de contabilidad"""
    # Obtener estadísticas básicas
    total_cuentas = Cuenta.objects.count()
    total_asientos = Asiento.objects.count()
    ultimos_asientos = Asiento.objects.all().order_by('-fecha')[:5]
    
    context = {
        'total_cuentas': total_cuentas,
        'total_asientos': total_asientos,
        'ultimos_asientos': ultimos_asientos,
    }
    return render(request, 'contabilidad/index.html', context)

# -------------------------
# CATÁLOGO DE CUENTAS
# -------------------------
@login_required(login_url='/login/')
def catalogo_cuentas(request):
    """Vista del catálogo de cuentas"""
    cuentas = Cuenta.objects.all().order_by('codigo')
    context = {
        'cuentas': cuentas
    }
    return render(request, 'contabilidad/catalogo_cuentas.html', context)

# -------------------------
# DETALLE DE CUENTA
# -------------------------
@login_required(login_url='/login/')
def detalle_cuenta(request, pk):
    """Vista de detalle de una cuenta específica"""
    cuenta = get_object_or_404(Cuenta, pk=pk)
    
    # Obtener movimientos de esta cuenta
    movimientos = cuenta.partidas.select_related('asiento').order_by('-asiento__fecha')
    
    # Calcular totales
    total_debe = sum(mov.debe for mov in movimientos)
    total_haber = sum(mov.haber for mov in movimientos)
    saldo_actual = cuenta.get_saldo()
    
    context = {
        'cuenta': cuenta,
        'movimientos': movimientos,
        'total_debe': total_debe,
        'total_haber': total_haber,
        'saldo_actual': saldo_actual,
    }
    
    return render(request, 'contabilidad/detalle_cuenta.html', context)

# -------------------------
# NUEVA TRANSACCIÓN
# -------------------------
@login_required(login_url='/login/')
def nueva_transaccion(request):
    """Vista para crear nueva transacción (asiento contable)"""
    cuentas = Cuenta.objects.filter(es_cuenta_detalle=True).order_by('codigo')
    
    # Obtener cuentas específicas para IVA
    cuenta_iva_pagar = Cuenta.objects.filter(
        nombre__icontains='iva', 
        tipo='pasivo'
    ).first()
    
    cuenta_iva_cobrar = Cuenta.objects.filter(
        nombre__icontains='iva', 
        tipo='activo'
    ).first()
    
    # Si no existen, crearlas automáticamente
    if not cuenta_iva_pagar:
        cuenta_iva_pagar = Cuenta.objects.create(
            codigo='2105',
            nombre='IVA Por Pagar',
            tipo='pasivo',
            descripcion='Impuesto al Valor Agregado por pagar',
            es_cuenta_detalle=True
        )
    
    if not cuenta_iva_cobrar:
        cuenta_iva_cobrar = Cuenta.objects.create(
            codigo='1106',
            nombre='IVA Por Cobrar',
            tipo='activo',
            descripcion='Impuesto al Valor Agregado por cobrar',
            es_cuenta_detalle=True
        )
    
    context = {
        'cuentas': cuentas,
        'fecha_actual': timezone.now().strftime('%Y-%m-%d'),
        'cuenta_iva_pagar': cuenta_iva_pagar,
        'cuenta_iva_cobrar': cuenta_iva_cobrar,
        'cuenta_iva_pagar_id': cuenta_iva_pagar.id if cuenta_iva_pagar else None,
        'cuenta_iva_cobrar_id': cuenta_iva_cobrar.id if cuenta_iva_cobrar else None,
    }
    return render(request, 'contabilidad/nueva_transaccion.html', context)

# -------------------------
# GUARDAR TRANSACCIÓN
# -------------------------
@login_required(login_url='/login/')
@require_POST
@csrf_exempt
def guardar_transaccion(request):
    """Vista para guardar la transacción vía AJAX"""
    try:
        data = json.loads(request.body)
        movimientos = data.get('movimientos', [])
        descripcion_general = data.get('descripcion_general', '')
        fecha = data.get('fecha', timezone.now().date())
        
        # Validaciones básicas
        if not descripcion_general:
            return JsonResponse({
                'success': False,
                'message': 'La descripción general es requerida'
            })
            
        if len(movimientos) < 2:
            return JsonResponse({
                'success': False,
                'message': 'Debe haber al menos 2 movimientos (débito y crédito)'
            })
        
        # Validar que el asiento esté balanceado
        total_debe = sum(Decimal(mov['debe']) for mov in movimientos)
        total_haber = sum(Decimal(mov['haber']) for mov in movimientos)
        
        if total_debe != total_haber:
            return JsonResponse({
                'success': False,
                'message': f'El asiento no está balanceado. Débito: {total_debe}, Crédito: {total_haber}'
            })
        
        # Verificar si el asiento tiene IVA
        tiene_iva = any(mov.get('es_iva', False) for mov in movimientos)
        
        # Crear el asiento
        asiento = Asiento.objects.create(
            fecha=fecha,
            descripcion=descripcion_general,
            creado_por=request.user,
            tiene_iva=tiene_iva,
            monto_total=total_debe + total_haber
        )
        
        # Crear las partidas
        for mov in movimientos:
            cuenta = get_object_or_404(Cuenta, id=mov['cuenta_id'])
            Partida.objects.create(
                asiento=asiento,
                cuenta=cuenta,
                debe=mov['debe'],
                haber=mov['haber'],
                descripcion=mov['descripcion'],
                es_iva=mov.get('es_iva', False),
                monto_base=mov.get('monto_base', 0),
                monto_iva=mov.get('monto_iva', 0)
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Transacción guardada exitosamente',
            'asiento_id': asiento.id,
            'tiene_iva': tiene_iva
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar la transacción: {str(e)}'
        })

# -------------------------
# LIBRO DIARIO
# -------------------------
@login_required(login_url='/login/')
def libro_diario(request):
    """Vista para mostrar el libro diario"""
    asientos = Asiento.objects.all().order_by('-fecha', '-id')[:50]  # Últimos 50 asientos
    return render(request, 'contabilidad/libro_diario.html', {'asientos': asientos})

# -------------------------
# DETALLE DE ASIENTO
# -------------------------
@login_required(login_url='/login/')
def detalle_asiento(request, asiento_id):
    """Vista para ver el detalle de un asiento específico"""
    asiento = get_object_or_404(Asiento, id=asiento_id)
    partidas = asiento.partidas.all()
    
    context = {
        'asiento': asiento,
        'partidas': partidas,
    }
    return render(request, 'contabilidad/detalle_asiento.html', context)