from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
import json
from decimal import Decimal
from .models import Cuenta, Asiento, Partida
from django.utils import timezone
from django.db import transaction


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
    # Se recomienda usar snake_case en el nombre del template
   

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
    # Obtener cuentas de IVA si existen
    try:
        cuenta_iva_pagar = Cuenta.objects.get(nombre__icontains='iva debito')
        cuenta_iva_pagar_id = cuenta_iva_pagar.id
    except Cuenta.DoesNotExist:
        cuenta_iva_pagar_id = None

    try:
        cuenta_iva_cobrar = Cuenta.objects.get(nombre__icontains='iva credito')
        cuenta_iva_cobrar_id = cuenta_iva_cobrar.id
    except Cuenta.DoesNotExist:
        cuenta_iva_cobrar_id = None

    context = {
        'fecha_actual': timezone.now().date().isoformat(),
        'cuentas': Cuenta.objects.filter(es_cuenta_detalle=True),
        'cuenta_iva_pagar_id': cuenta_iva_pagar_id,
        'cuenta_iva_cobrar_id': cuenta_iva_cobrar_id,
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
        descripcion_general = data.get('descripcion_general', '').strip()
        fecha_str = data.get('fecha')
        
        print(f"📥 Datos recibidos - Movimientos: {len(movimientos)}, Descripción: {descripcion_general}")

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
        
        # Validar fecha
        if fecha_str:
            fecha = timezone.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            fecha = timezone.now().date()
        
        # Validar que el asiento esté balanceado
        total_debe = sum(Decimal(str(mov['debe'])) for mov in movimientos)
        total_haber = sum(Decimal(str(mov['haber'])) for mov in movimientos)
        
        diferencia = abs(total_debe - total_haber)
        if diferencia > Decimal('0.01'):  # Tolerancia para decimales
            return JsonResponse({
                'success': False,
                'message': f'El asiento no está balanceado. Débito: ${total_debe:.2f}, Crédito: ${total_haber:.2f}, Diferencia: ${diferencia:.2f}'
            })
        
        # Verificar si el asiento tiene IVA
        tiene_iva = any(mov.get('es_iva', False) for mov in movimientos)
        
        # Usar transacción atómica para asegurar consistencia
        with transaction.atomic():
            # Crear el asiento
            asiento = Asiento.objects.create(
                fecha=fecha,
                descripcion=descripcion_general,
                creado_por=request.user,
                tiene_iva=tiene_iva,
                monto_total=total_debe  # Usar total_debe ya que debe = haber
            )
            
            # Crear las partidas
            partidas_creadas = 0
            for mov in movimientos:
                try:
                    cuenta = Cuenta.objects.get(id=mov['cuenta_id'])
                    
                    Partida.objects.create(
                        asiento=asiento,
                        cuenta=cuenta,
                        debe=Decimal(str(mov['debe'])),
                        haber=Decimal(str(mov['haber'])),
                        descripcion=mov.get('descripcion', '')[:200],  # Limitar longitud
                        es_iva=mov.get('es_iva', False),
                        monto_base=Decimal(str(mov.get('monto_base', 0))),
                        monto_iva=Decimal(str(mov.get('monto_iva', 0)))
                    )
                    partidas_creadas += 1
                    
                except Cuenta.DoesNotExist:
                    # Continuar con otras partidas si una cuenta no existe
                    continue
                except Exception as e:
                    # Log del error pero continuar
                    print(f"Error creando partida: {e}")
                    continue
            
            # Verificar que se crearon partidas
            if partidas_creadas == 0:
                raise Exception("No se pudo crear ninguna partida")
        
        return JsonResponse({
            'success': True,
            'message': f'Transacción #{asiento.id} guardada exitosamente',
            'asiento_id': asiento.id,
            'tiene_iva': tiene_iva,
            'partidas_creadas': partidas_creadas
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error en el formato de los datos enviados'
        })
        
    except Exception as e:
        print(f"❌ Error en guardar_transaccion: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar la transacción: {str(e)}'
        })


# -------------------------
# LIBRO MAYOR - CORREGIDA
# -------------------------
@login_required(login_url='/login/')
def libro_mayor(request):
    """Vista para mostrar el libro mayor"""
    selected_cuenta = request.GET.get('cuenta', '')
    
    # Obtener todas las cuentas para el dropdown
    todas_las_cuentas = Cuenta.objects.filter(es_cuenta_detalle=True).values_list('nombre', flat=True).distinct()
    
    cuentas_data = []
    total_debe = 0
    total_haber = 0
    saldo_acumulado = 0
    
    if selected_cuenta:
        try:
            # Obtener la cuenta específica
            cuenta_obj = Cuenta.objects.get(nombre=selected_cuenta)
            
            # Obtener todas las partidas de esta cuenta
            partidas = Partida.objects.filter(cuenta=cuenta_obj).select_related('asiento').order_by('asiento__fecha', 'asiento__id')
            
            for partida in partidas:
                debe = float(partida.debe)
                haber = float(partida.haber)
                
                # Calcular saldo acumulado
                if cuenta_obj.tipo in ['activo', 'gastos']:
                    saldo_acumulado += debe - haber
                else:  # pasivo, capital, ingresos
                    saldo_acumulado += haber - debe
                
                cuentas_data.append({
                    'fecha': partida.asiento.fecha,
                    'numero': partida.asiento.id,
                    'descripcion': partida.descripcion or partida.asiento.descripcion,
                    'debe': debe,
                    'haber': haber,
                    'saldo': saldo_acumulado
                })
                
                total_debe += debe
                total_haber += haber
                
        except Cuenta.DoesNotExist:
            # Si la cuenta no existe, mostrar mensaje
            pass
    
    context = {
        'selected_cuenta': selected_cuenta,
        'todas_las_cuentas': todas_las_cuentas,
        'cuentas': cuentas_data,
        'totales': {
            'total_debe': total_debe,
            'total_haber': total_haber,
            'total_saldo': saldo_acumulado
        }
    }
    return render(request, 'contabilidad/libro_mayor.html', context)

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
# Inventario de Licencias
# -------------------------

def planilla(request):
    return render(request, 'contabilidad/planilla.html')

# -------------------------
# API PARA CATÁLOGO DE CUENTAS
# -------------------------
@login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_cuentas(request):
    """API para manejar cuentas contables"""
    if request.method == 'GET':
        # Obtener todas las cuentas
        cuentas = list(Cuenta.objects.all().values('id', 'codigo', 'nombre', 'tipo', 'descripcion', 'grupo'))
        return JsonResponse(cuentas, safe=False)
    
    elif request.method == 'POST':
        # Crear nueva cuenta
        try:
            data = json.loads(request.body)
            
            # Validar que el código no exista
            if Cuenta.objects.filter(codigo=data['codigo']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe una cuenta con este código'
                }, status=400)
            
            cuenta = Cuenta.objects.create(
                codigo=data['codigo'],
                nombre=data['nombre'],
                tipo=data['tipo'].lower(),  # Convertir a minúsculas para coincidir con tu modelo
                descripcion=data.get('descripcion', ''),
                grupo=data.get('grupo', ''),
                es_cuenta_detalle=True
            )
            
            return JsonResponse({
                'success': True,
                'id': cuenta.id,
                'message': 'Cuenta creada exitosamente'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al crear la cuenta: {str(e)}'
            }, status=400)

@login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def api_cuenta_detalle(request, cuenta_id):
    """API para editar y eliminar cuentas específicas"""
    try:
        cuenta = Cuenta.objects.get(id=cuenta_id)
        
        if request.method == 'PUT':
            # Actualizar cuenta
            data = json.loads(request.body)
            
            # Validar que el código no esté duplicado (excluyendo la cuenta actual)
            if Cuenta.objects.filter(codigo=data['codigo']).exclude(id=cuenta_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe otra cuenta con este código'
                }, status=400)
            
            cuenta.codigo = data['codigo']
            cuenta.nombre = data['nombre']
            cuenta.tipo = data['tipo'].lower()
            cuenta.descripcion = data.get('descripcion', '')
            cuenta.grupo = data.get('grupo', '')
            cuenta.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Cuenta actualizada exitosamente'
            })
        
        elif request.method == 'DELETE':
            # Eliminar cuenta
            # Verificar si la cuenta tiene movimientos
            if cuenta.partidas.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede eliminar la cuenta porque tiene movimientos asociados'
                }, status=400)
            
            cuenta.delete()
            return JsonResponse({
                'success': True,
                'message': 'Cuenta eliminada exitosamente'
            })
            
    except Cuenta.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Cuenta no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=400)
