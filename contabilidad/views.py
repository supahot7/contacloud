# views.py - VERSIÓN COMPLETA CORREGIDA
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
import json
from decimal import Decimal
from .models import Cuenta, Asiento, Partida, Licencia
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, Q
from datetime import datetime


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
# Estados Financieros
# -------------------------
@login_required(login_url='/login/')
def estados_financieros(request):
    return render(request, 'contabilidad/estadosFinancieros.html')

# -------------------------
# Balance General - CON DATOS REALES
# -------------------------
#@login_required(login_url='/login/')
def balance_general(request):
    """Balance General con datos reales de la contabilidad"""
    from django.db.models import Sum, Q
    from datetime import datetime
    
    # Obtener filtros de fecha
    fecha_inicial = request.GET.get('fecha_inicial', '2025-01-01')
    fecha_final = request.GET.get('fecha_final', datetime.now().strftime('%Y-%m-%d'))
    
    # Función para calcular saldo de una cuenta
    def calcular_saldo(cuenta_tipo):
        cuentas = Cuenta.objects.filter(
            tipo=cuenta_tipo,
            es_cuenta_detalle=True
        )
        
        resultados = []
        total = 0
        
        for cuenta in cuentas:
            partidas = Partida.objects.filter(
                cuenta=cuenta,
                asiento__fecha__range=[fecha_inicial, fecha_final],
                asiento__estado='contabilizado'
            )
            
            debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
            haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
            
            # Calcular saldo según naturaleza de la cuenta
            if cuenta_tipo in ['activo', 'gasto']:
                saldo = debe - haber
            else:  # pasivo, capital, ingreso
                saldo = haber - debe
            
            if saldo != 0:  # Solo mostrar cuentas con movimiento
                resultados.append({
                    'codigo': cuenta.codigo,
                    'nombre': cuenta.nombre,
                    'debe': debe if debe > haber else 0,
                    'haber': haber if haber > debe else 0,
                    'saldo': abs(saldo)
                })
                total += abs(saldo)
        
        return resultados, total
    
    # Calcular por cada tipo de cuenta
    activos, total_activos = calcular_saldo('activo')
    pasivos, total_pasivos = calcular_saldo('pasivo')
    capital, total_capital = calcular_saldo('capital')
    
    # Verificar balance
    total_debe = total_activos
    total_haber = total_pasivos + total_capital
    esta_balanceado = abs(total_debe - total_haber) < 0.01
    
    context = {
        'fecha_inicial': fecha_inicial,
        'fecha_final': fecha_final,
        'activos': activos,
        'pasivos': pasivos,
        'capital': capital,
        'total_activos': total_activos,
        'total_pasivos': total_pasivos,
        'total_capital': total_capital,
        'total_debe': total_debe,
        'total_haber': total_haber,
        'esta_balanceado': esta_balanceado,
    }
    
    return render(request, 'contabilidad/balanceGeneral.html', context)

# -------------------------
# Estado de Resultados
# -------------------------
@login_required(login_url='/login/')
def estado_resultados(request):
    """Estado de Resultados con datos reales de la contabilidad"""
    from datetime import datetime
    
    # Obtener filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio', '2025-01-01')
    fecha_fin = request.GET.get('fecha_fin', datetime.now().strftime('%Y-%m-%d'))
    
    # Función para obtener cuentas con saldo
    def obtener_cuentas_con_saldo(tipo_cuenta):
        cuentas = Cuenta.objects.filter(
            tipo=tipo_cuenta,
            es_cuenta_detalle=True
        )
        
        resultados = []
        total = 0
        
        for cuenta in cuentas:
            partidas = Partida.objects.filter(
                cuenta=cuenta,
                asiento__fecha__range=[fecha_inicio, fecha_fin],
                asiento__estado='contabilizado'
            )
            
            debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
            haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
            
            # Para ingresos: haber - debe (naturaleza acreedora)
            # Para gastos: debe - haber (naturaleza deudora)
            if tipo_cuenta == 'ingreso':
                saldo = haber - debe
            else:  # gasto
                saldo = debe - haber
            
            if saldo > 0:
                resultados.append({
                    'nombre': f"{cuenta.codigo} - {cuenta.nombre}",
                    'monto': saldo
                })
                total += saldo
        
        return resultados, total
    
    # Obtener datos
    ingresos, total_ingresos = obtener_cuentas_con_saldo('ingreso')
    gastos, total_gastos = obtener_cuentas_con_saldo('gasto')
    
    # Calcular utilidad/pérdida neta
    utilidad_neta = total_ingresos - total_gastos
    
    # Determinar si es utilidad o pérdida
    if utilidad_neta >= 0:
        nombre_utilidad = 'UTILIDAD NETA'
        clase_utilidad = 'table-success'
    else:
        nombre_utilidad = 'PÉRDIDA NETA'
        clase_utilidad = 'table-danger'
    
    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'ingresos': ingresos,
        'total_ingresos': total_ingresos,
        'gastos': gastos,
        'total_gastos': total_gastos,
        'utilidad_neta': abs(utilidad_neta),
        'nombre_utilidad': nombre_utilidad,
        'clase_utilidad': clase_utilidad,
        # No hay costos separados en tu catálogo, así que los dejamos vacíos
        'costos': [],
        'total_costos': 0,
        'utilidad_bruta': total_ingresos,  # Sin costos, utilidad bruta = ingresos
    }
    
    return render(request, 'contabilidad/estadoResultados.html', context)

# -------------------------
# Estado de Capital
# -------------------------
@login_required(login_url='/login/')
def estado_capital(request):
    """Estado de Capital con datos reales de la contabilidad"""
    from datetime import datetime
    
    # Obtener filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio', '2025-01-01')
    fecha_fin = request.GET.get('fecha_fin', datetime.now().strftime('%Y-%m-%d'))
    
    # Obtener cuentas de capital
    cuentas_capital = Cuenta.objects.filter(
        tipo='capital',
        es_cuenta_detalle=True
    )
    
    capital_inicial_monto = 0
    aumentos = []
    total_aumentos = 0
    
    for cuenta in cuentas_capital:
        partidas = Partida.objects.filter(
            cuenta=cuenta,
            asiento__fecha__range=[fecha_inicio, fecha_fin],
            asiento__estado='contabilizado'
        )
        
        debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
        haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
        saldo = haber - debe  # Capital tiene naturaleza acreedora
        
        if saldo > 0:
            if 'capital social' in cuenta.nombre.lower():
                capital_inicial_monto = saldo
            else:
                aumentos.append({
                    'nombre': f"{cuenta.codigo} - {cuenta.nombre}",
                    'monto': saldo
                })
                total_aumentos += saldo
    
    # Obtener utilidad del período desde Estado de Resultados
    ingresos_total = Cuenta.objects.filter(tipo='ingreso', es_cuenta_detalle=True)
    gastos_total = Cuenta.objects.filter(tipo='gasto', es_cuenta_detalle=True)
    
    total_ing = 0
    for cuenta in ingresos_total:
        partidas = Partida.objects.filter(
            cuenta=cuenta,
            asiento__fecha__range=[fecha_inicio, fecha_fin],
            asiento__estado='contabilizado'
        )
        debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
        haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
        total_ing += (haber - debe)
    
    total_gast = 0
    for cuenta in gastos_total:
        partidas = Partida.objects.filter(
            cuenta=cuenta,
            asiento__fecha__range=[fecha_inicio, fecha_fin],
            asiento__estado='contabilizado'
        )
        debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
        haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
        total_gast += (debe - haber)
    
    utilidad_periodo = total_ing - total_gast
    
    if utilidad_periodo > 0:
        aumentos.append({
            'nombre': 'Utilidad del ejercicio',
            'monto': utilidad_periodo
        })
        total_aumentos += utilidad_periodo
    
    # Calcular capital final
    capital_final = capital_inicial_monto + total_aumentos
    
    # Determinar clase CSS
    if capital_final >= capital_inicial_monto:
        nombre_capital_final = 'CAPITAL FINAL'
        clase_capital = 'table-success'
    else:
        nombre_capital_final = 'CAPITAL FINAL (DISMINUIDO)'
        clase_capital = 'table-warning'
    
    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'capital_inicial': {
            'nombre': 'Capital Social',
            'monto': capital_inicial_monto
        },
        'aumentos_capital': aumentos,
        'total_aumentos': total_aumentos,
        'disminuciones_capital': [],  # Por ahora vacío
        'total_disminuciones': 0,
        'capital_final': capital_final,
        'nombre_capital_final': nombre_capital_final,
        'clase_capital': clase_capital,
    }
    
    return render(request, 'contabilidad/estadoCapital.html', context)

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
    saldo_actual = 0  # Esta función get_saldo() no existe en tu modelo, la removí
    
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
    """Vista para guardar la transacción vía AJAX - CON ACTUALIZACIÓN DE INVENTARIO"""
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
        if diferencia > Decimal('0.01'):
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
                monto_total=total_debe
            )
            
            # Crear las partidas Y actualizar inventario
            partidas_creadas = 0
            inventario_actualizado = False
            
            for mov in movimientos:
                try:
                    cuenta = Cuenta.objects.get(id=mov['cuenta_id'])
                    
                    Partida.objects.create(
                        asiento=asiento,
                        cuenta=cuenta,
                        debe=Decimal(str(mov['debe'])),
                        haber=Decimal(str(mov['haber'])),
                        descripcion=mov.get('descripcion', '')[:200],
                        es_iva=mov.get('es_iva', False),
                        monto_base=Decimal(str(mov.get('monto_base', 0))),
                        monto_iva=Decimal(str(mov.get('monto_iva', 0)))
                    )
                    partidas_creadas += 1
                    
                    # ============================================
                    # ACTUALIZAR INVENTARIO AUTOMÁTICAMENTE
                    # ============================================
                    if 'inventario de licencias' in cuenta.nombre.lower():
                        monto_haber = Decimal(str(mov['haber']))
                        
                        # Si hay un HABER en inventario = SALIDA (venta)
                        if monto_haber > 0:
                            # Buscar licencias disponibles
                            licencias_disponibles = Licencia.objects.filter(
                                cantidad_disponible__gt=0
                            ).order_by('fecha_adquisicion')
                            
                            if licencias_disponibles.exists():
                                # Usar el costo promedio o el de la primera licencia
                                licencia_ref = licencias_disponibles.first()
                                costo_unitario = licencia_ref.costo_unitario
                                
                                if costo_unitario > 0:
                                    cantidad_a_vender = int(monto_haber / costo_unitario)
                                    
                                    for licencia in licencias_disponibles:
                                        if cantidad_a_vender <= 0:
                                            break
                                        
                                        cantidad_en_esta = min(cantidad_a_vender, licencia.cantidad_disponible)
                                        licencia.vender_licencias(cantidad_en_esta)
                                        cantidad_a_vender -= cantidad_en_esta
                                        inventario_actualizado = True
                                        
                                        print(f"📦 Inventario actualizado: Vendidas {cantidad_en_esta} de {licencia.nombre}")
                    
                except Cuenta.DoesNotExist:
                    continue
                except Exception as e:
                    print(f"Error creando partida: {e}")
                    continue
            
            if partidas_creadas == 0:
                raise Exception("No se pudo crear ninguna partida")
        
        mensaje_respuesta = f'Transacción #{asiento.id} guardada exitosamente'
        if inventario_actualizado:
            mensaje_respuesta += '. El inventario de licencias fue actualizado automáticamente.'
        
        return JsonResponse({
            'success': True,
            'message': mensaje_respuesta,
            'asiento_id': asiento.id,
            'tiene_iva': tiene_iva,
            'partidas_creadas': partidas_creadas,
            'inventario_actualizado': inventario_actualizado
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
# LIBRO MAYOR - VERSIÓN CORREGIDA PARA MOSTRAR TODOS LOS ASIENTOS
# -------------------------
@login_required(login_url='/login/')
def libro_mayor(request):
    """Vista para mostrar el libro mayor, permitiendo ver todos los asientos."""
    selected_cuenta = request.GET.get('cuenta', '')
    
    # Obtener todas las cuentas detalle para el selector
    todas_las_cuentas = Cuenta.objects.filter(es_cuenta_detalle=True).values_list('nombre', flat=True).distinct()
    
    cuentas_data = []
    total_debe = 0
    total_haber = 0
    
    # --- Lógica principal ---
    
    if selected_cuenta:
        # Caso 1: Se seleccionó una cuenta específica (la lógica original se mantiene)
        try:
            cuenta_obj = Cuenta.objects.get(nombre=selected_cuenta)
            
            # Filtra las partidas por esa cuenta y las ordena por fecha y ID de asiento
            partidas = Partida.objects.filter(cuenta=cuenta_obj).select_related('asiento').order_by('asiento__fecha', 'asiento__id')
            
            saldo_acumulado = 0
            
            for partida in partidas:
                debe = float(partida.debe)
                haber = float(partida.haber)
                
                # Cálculo del saldo acumulado según la naturaleza de la cuenta
                if cuenta_obj.tipo in ['activo', 'gasto']:
                    saldo_acumulado += debe - haber
                else:
                    saldo_acumulado += haber - debe
                
                cuentas_data.append({
                    'fecha': partida.asiento.fecha,
                    'numero': partida.asiento.id,
                    'descripcion': partida.descripcion or partida.asiento.descripcion,
                    'debe': debe,
                    'haber': haber,
                    'saldo': saldo_acumulado # Saldo acumulado para la cuenta seleccionada
                })
                
                total_debe += debe
                total_haber += haber
                
        except Cuenta.DoesNotExist:
            pass # No hace nada si la cuenta no existe
    
    elif not selected_cuenta and 'cuenta' in request.GET:
        # Caso 2: Se seleccionó "-- Todas las cuentas --" (cuando 'cuenta' está en GET pero vacío)
        
        # Obtener TODAS las partidas de TODOS los asientos, ordenadas por fecha y asiento
        todas_las_partidas = Partida.objects.select_related('asiento', 'cuenta').order_by('asiento__fecha', 'asiento__id')
        
        # Al mostrar "Todas las cuentas", el "Saldo Acumulado" por fila no tiene sentido (pues el saldo es por cuenta).
        # Por lo tanto, solo mostraremos los movimientos y los totales generales (Debe y Haber).
        
        for partida in todas_las_partidas:
            debe = float(partida.debe)
            haber = float(partida.haber)
            
            cuentas_data.append({
                'fecha': partida.asiento.fecha,
                'numero': partida.asiento.id,
                # Mostramos la cuenta a la que afecta el movimiento
                'descripcion': f"[{partida.cuenta.codigo} - {partida.cuenta.nombre}] | {partida.descripcion or partida.asiento.descripcion}", 
                'debe': debe,
                'haber': haber,
                'saldo': None # No se calcula saldo acumulado en esta vista
            })
            
            total_debe += debe
            total_haber += haber
            
        # El saldo final no se calcula aquí, ya que el reporte muestra todas las cuentas.
        saldo_acumulado = total_debe - total_haber 
        
    # --- Contexto ---
    context = {
        'selected_cuenta': selected_cuenta,
        'todas_las_cuentas': todas_las_cuentas,
        'cuentas': cuentas_data,
        'totales': {
            'total_debe': total_debe,
            'total_haber': total_haber,
            # Se usa el saldo para la alerta solo si se seleccionó una cuenta específica
            'total_saldo': saldo_acumulado if selected_cuenta else total_debe - total_haber 
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

# -------------------------
# Planilla
# -------------------------
def planilla(request):
    return render(request, 'contabilidad/planilla.html')


# -------------------------
# APIS PARA CUENTAS
# -------------------------
@login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_cuentas(request):
    """API para manejar cuentas contables"""
    if request.method == 'GET':
        cuentas = list(Cuenta.objects.all().values('id', 'codigo', 'nombre', 'tipo', 'descripcion', 'grupo'))
        return JsonResponse(cuentas, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if Cuenta.objects.filter(codigo=data['codigo']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe una cuenta con este código'
                }, status=400)
            
            cuenta = Cuenta.objects.create(
                codigo=data['codigo'],
                nombre=data['nombre'],
                tipo=data['tipo'].lower(),
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
            data = json.loads(request.body)
            
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

# -------------------------
# INVENTARIO DE LICENCIAS (Vista principal)
# -------------------------
@login_required(login_url='/login/')
def inventario_licencias(request):
    """Vista del inventario de licencias con datos reales"""
    licencias = Licencia.objects.all().order_by('-creado_en')
    
    # Calcular totales
    total_licencias = licencias.count()
    unidades_disponibles = sum(lic.cantidad_disponible for lic in licencias)
    valor_total_inventario = sum(float(lic.valor_total_inventario) for lic in licencias)
    
    context = {
        'licencias': licencias,
        'total_licencias': total_licencias,
        'unidades_disponibles': unidades_disponibles,
        'valor_total_inventario': valor_total_inventario,
    }
    return render(request, 'contabilidad/inventarioLicencias.html', context)

# -------------------------
# APIS PARA LICENCIAS - CORREGIDAS
# -------------------------
# views.py - ACTUALIZAR LAS APIS
@login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_licencias(request):
    """API para manejar licencias - ACTUALIZADA"""
    if request.method == 'GET':
        try:
            licencias = list(Licencia.objects.all().values(
                'id', 'codigo', 'nombre', 'descripcion', 
                'fecha_adquisicion', 'costo_unitario',
                'cantidad_total', 'cantidad_disponible', 'estado',
                'valor_total_inventario_db',  # NUEVO CAMPO
                'creado_en'
            ))
            return JsonResponse(licencias, safe=False)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al cargar licencias: {str(e)}'
            }, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validaciones
            if not data.get('codigo') or not data.get('nombre'):
                return JsonResponse({
                    'success': False,
                    'message': 'El código y nombre son obligatorios'
                }, status=400)
            
            if Licencia.objects.filter(codigo=data['codigo']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe una licencia con este código'
                }, status=400)
            
            # Crear licencia
            licencia = Licencia.objects.create(
                codigo=data['codigo'],
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                fecha_adquisicion=data.get('fecha_adquisicion', timezone.now().date()),
                costo_unitario=Decimal(str(data.get('costo_unitario', 0))),
                cantidad_total=int(data.get('cantidad_total', 1)),
                cantidad_disponible=int(data.get('cantidad_total', 1)),
                creado_por=request.user
                # valor_total_inventario_db se calcula automáticamente en save()
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Licencia creada exitosamente',
                'id': licencia.id,
                'codigo': licencia.codigo,
                'valor_total_inventario': float(licencia.valor_total_inventario_db)
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error en el formato JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al crear licencia: {str(e)}'
            }, status=400)

@login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_licencia_detalle(request, licencia_id):
    """API para obtener, editar y eliminar licencias específicas - ACTUALIZADA"""
    try:
        licencia = Licencia.objects.get(id=licencia_id)
        
        if request.method == 'GET':
            licencia_data = {
                'id': licencia.id,
                'codigo': licencia.codigo,
                'nombre': licencia.nombre,
                'descripcion': licencia.descripcion,
                'fecha_adquisicion': licencia.fecha_adquisicion.isoformat(),
                'costo_unitario': float(licencia.costo_unitario),
                'cantidad_total': licencia.cantidad_total,
                'cantidad_disponible': licencia.cantidad_disponible,
                'estado': licencia.estado,
                'valor_total_inventario': float(licencia.valor_total_inventario_db),  # USAR EL CAMPO DE BD
                'creado_en': licencia.creado_en.isoformat(),
            }
            return JsonResponse(licencia_data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            
            # Validaciones
            if not data.get('codigo') or not data.get('nombre'):
                return JsonResponse({
                    'success': False,
                    'message': 'El código y nombre son obligatorios'
                }, status=400)
            
            if Licencia.objects.filter(codigo=data['codigo']).exclude(id=licencia_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe otra licencia con este código'
                }, status=400)
            
            # Actualizar licencia
            licencia.codigo = data['codigo']
            licencia.nombre = data['nombre']
            licencia.descripcion = data.get('descripcion', '')
            
            # Manejar fecha
            if data.get('fecha_adquisicion'):
                licencia.fecha_adquisicion = data['fecha_adquisicion']
            
            licencia.costo_unitario = Decimal(str(data.get('costo_unitario', 0)))
            
            # Manejar cantidad total - ajustar cantidad disponible si es necesario
            nueva_cantidad_total = int(data.get('cantidad_total', 1))
            diferencia = nueva_cantidad_total - licencia.cantidad_total
            licencia.cantidad_total = nueva_cantidad_total
            licencia.cantidad_disponible = max(0, licencia.cantidad_disponible + diferencia)
            
            # El valor_total_inventario_db se actualiza automáticamente en save()
            
            # Actualizar estado si es necesario
            if licencia.cantidad_disponible == 0:
                licencia.estado = 'vendida'
            elif licencia.estado == 'vendida' and licencia.cantidad_disponible > 0:
                licencia.estado = 'disponible'
            
            licencia.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Licencia actualizada exitosamente',
                'valor_total_inventario': float(licencia.valor_total_inventario_db)
            })
        
        elif request.method == 'DELETE':
            licencia.delete()
            return JsonResponse({
                'success': True,
                'message': 'Licencia eliminada exitosamente'
            })
            
    except Licencia.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Licencia no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=400)
@login_required(login_url='/login/')
@csrf_exempt
@require_POST
def api_licencia_agregar_stock(request, licencia_id):
    """API para agregar stock a una licencia - CORREGIDA"""
    try:
        licencia = Licencia.objects.get(id=licencia_id)
        data = json.loads(request.body)
        cantidad = int(data.get('cantidad', 0))
        
        if cantidad <= 0:
            return JsonResponse({
                'success': False,
                'message': 'La cantidad debe ser mayor a 0'
            }, status=400)
        
        # Usar el método del modelo para agregar licencias
        licencia.agregar_licencias(cantidad)
        
        return JsonResponse({
            'success': True,
            'message': f'Se agregaron {cantidad} licencias al inventario. Total disponible: {licencia.cantidad_disponible}',
            'nueva_cantidad': licencia.cantidad_disponible
        })
        
    except Licencia.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Licencia no encontrada'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error en el formato JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al agregar stock: {str(e)}'
        }, status=400)

# -------------------------
# API adicional para obtener datos del dashboard
# -------------------------
@login_required(login_url='/login/')
def api_licencias_dashboard(request):
    """API para obtener datos resumidos del inventario - CORREGIDA"""
    try:
        licencias = Licencia.objects.all()
        
        total_licencias = licencias.count()
        unidades_disponibles = sum(lic.cantidad_disponible for lic in licencias)
        
        # CORRECCIÓN: Usar el campo que está en la base de datos
        valor_total_inventario = sum(float(lic.valor_total_inventario_db) for lic in licencias)
        
        # Licencias por estado
        licencias_por_estado = {
            'disponible': licencias.filter(estado='disponible').count(),
            'vendida': licencias.filter(estado='vendida').count(),
            'inactiva': licencias.filter(estado='inactiva').count(),
        }
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_licencias': total_licencias,
                'unidades_disponibles': unidades_disponibles,
                'valor_total_inventario': valor_total_inventario,
                'licencias_por_estado': licencias_por_estado
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar datos del dashboard: {str(e)}'
        }, status=500)
    

    # -------------------------
# Cierre Contable - VISTAS NUEVAS
# -------------------------
@login_required(login_url='/login/')
def cierre_contable(request):
    """Vista principal del cierre contable"""
    from datetime import datetime
    
    # Obtener parámetros
    ano_seleccionado = request.GET.get('ano_cierre', str(datetime.now().year))
    fecha_cierre = request.GET.get('fecha_cierre', f'{ano_seleccionado}-12-31')
    
    # Obtener años disponibles (últimos 5 años)
    anos_disponibles = [str(year) for year in range(datetime.now().year - 4, datetime.now().year + 1)]
    
    # Calcular saldos para el cierre
    fecha_inicio = f'{ano_seleccionado}-01-01'
    fecha_fin = fecha_cierre
    
    # Obtener cuentas de ingresos y gastos
    def obtener_saldos_cuentas(tipo_cuenta):
        cuentas = Cuenta.objects.filter(
            tipo=tipo_cuenta,
            es_cuenta_detalle=True
        )
        
        resultados = []
        for cuenta in cuentas:
            partidas = Partida.objects.filter(
                cuenta=cuenta,
                asiento__fecha__range=[fecha_inicio, fecha_fin],
                asiento__estado='contabilizado'
            )
            
            debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
            haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
            
            if tipo_cuenta == 'ingreso':
                saldo = haber - debe  # Naturaleza acreedora
            else:  # gasto
                saldo = debe - haber  # Naturaleza deudora
            
            if saldo != 0:
                resultados.append({
                    'id': cuenta.id,
                    'codigo': cuenta.codigo,
                    'nombre': cuenta.nombre,
                    'saldo': abs(saldo),
                    'tipo': tipo_cuenta
                })
        
        return resultados
    
    cuentas_ingresos = obtener_saldos_cuentas('ingreso')
    cuentas_gastos = obtener_saldos_cuentas('gasto')
    
    # Calcular totales
    total_ingresos = sum(cuenta['saldo'] for cuenta in cuentas_ingresos)
    total_gastos = sum(cuenta['saldo'] for cuenta in cuentas_gastos)
    utilidad_neta = total_ingresos - total_gastos
    
    # Verificar si ya se realizó el cierre para este año
    cierre_realizado = Asiento.objects.filter(
        descripcion__icontains=f'cierre contable {ano_seleccionado}',
        tiene_iva=False
    ).exists()
    
    # Preparar asientos de cierre (simulación)
    asientos_cierre = []
    if not cierre_realizado:
        # Asiento para cerrar ingresos
        if total_ingresos > 0:
            asientos_cierre.append({
                'descripcion': 'Cierre de cuentas de ingresos',
                'monto': total_ingresos
            })
        
        # Asiento para cerrar gastos
        if total_gastos > 0:
            asientos_cierre.append({
                'descripcion': 'Cierre de cuentas de gastos',
                'monto': total_gastos
            })
        
        # Asiento de utilidad/pérdida
        if utilidad_neta != 0:
            tipo_resultado = 'Utilidad' if utilidad_neta > 0 else 'Pérdida'
            asientos_cierre.append({
                'descripcion': f'Traspaso de {tipo_resultado} neta a capital',
                'monto': abs(utilidad_neta)
            })
    
    # Verificar balance
    total_debe = total_gastos + (utilidad_neta if utilidad_neta > 0 else 0)
    total_haber = total_ingresos + (abs(utilidad_neta) if utilidad_neta < 0 else 0)
    esta_balanceado = abs(total_debe - total_haber) < 0.01
    diferencia_balance = abs(total_debe - total_haber)
    
    context = {
        'ano_seleccionado': ano_seleccionado,
        'fecha_cierre': fecha_cierre,
        'anos_disponibles': anos_disponibles,
        'cuentas_ingresos': cuentas_ingresos,
        'cuentas_gastos': cuentas_gastos,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'utilidad_neta': utilidad_neta,
        'cierre_realizado': cierre_realizado,
        'asientos_cierre': asientos_cierre,
        'total_cuentas_cierre': len(cuentas_ingresos) + len(cuentas_gastos),
        'esta_balanceado': esta_balanceado,
        'diferencia_balance': diferencia_balance,
        'total_debe': total_debe,
        'total_haber': total_haber,
    }
    
    return render(request, 'contabilidad/cierreContable.html', context)

@login_required(login_url='/login/')
@require_POST
@csrf_exempt
def ejecutar_cierre(request):
    """Ejecutar el cierre contable via AJAX"""
    try:
        data = json.loads(request.body)
        ano_cierre = data.get('ano_cierre')
        fecha_cierre = data.get('fecha_cierre')
        
        # Verificar que no se haya realizado ya el cierre
        if Asiento.objects.filter(descripcion__icontains=f'cierre contable {ano_cierre}').exists():
            return JsonResponse({
                'success': False,
                'message': f'El cierre contable para el año {ano_cierre} ya fue realizado'
            })
        
        # Obtener cuentas necesarias
        try:
            cuenta_utilidad_ejercicio = Cuenta.objects.get(nombre__icontains='utilidad del ejercicio')
        except Cuenta.DoesNotExist:
            # Crear cuenta si no existe
            cuenta_utilidad_ejercicio = Cuenta.objects.create(
                codigo='399',
                nombre='Utilidad del Ejercicio',
                tipo='capital',
                descripcion='Cuenta para el traspaso de resultados del ejercicio',
                es_cuenta_detalle=True
            )
        
        # Obtener saldos de cuentas de resultados
        fecha_inicio = f'{ano_cierre}-01-01'
        
        with transaction.atomic():
            # 1. Cerrar cuentas de ingresos
            cuentas_ingresos = Cuenta.objects.filter(tipo='ingreso', es_cuenta_detalle=True)
            for cuenta in cuentas_ingresos:
                partidas = Partida.objects.filter(
                    cuenta=cuenta,
                    asiento__fecha__range=[fecha_inicio, fecha_cierre],
                    asiento__estado='contabilizado'
                )
                
                debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
                haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
                saldo = haber - debe  # Naturaleza acreedora
                
                if saldo > 0:
                    # Crear asiento de cierre para esta cuenta de ingreso
                    asiento_cierre = Asiento.objects.create(
                        fecha=fecha_cierre,
                        descripcion=f'Cierre contable {ano_cierre} - {cuenta.nombre}',
                        creado_por=request.user,
                        tiene_iva=False,
                        monto_total=saldo
                    )
                    
                    # Partida 1: Cargo a la cuenta de ingreso (para cerrarla)
                    Partida.objects.create(
                        asiento=asiento_cierre,
                        cuenta=cuenta,
                        debe=saldo,
                        haber=0,
                        descripcion=f'Cierre de cuenta de ingreso {ano_cierre}'
                    )
                    
                    # Partida 2: Abono a utilidad del ejercicio
                    Partida.objects.create(
                        asiento=asiento_cierre,
                        cuenta=cuenta_utilidad_ejercicio,
                        debe=0,
                        haber=saldo,
                        descripcion=f'Traspaso a utilidad {ano_cierre}'
                    )
            
            # 2. Cerrar cuentas de gastos
            cuentas_gastos = Cuenta.objects.filter(tipo='gasto', es_cuenta_detalle=True)
            for cuenta in cuentas_gastos:
                partidas = Partida.objects.filter(
                    cuenta=cuenta,
                    asiento__fecha__range=[fecha_inicio, fecha_cierre],
                    asiento__estado='contabilizado'
                )
                
                debe = partidas.aggregate(total=Sum('debe'))['total'] or 0
                haber = partidas.aggregate(total=Sum('haber'))['total'] or 0
                saldo = debe - haber  # Naturaleza deudora
                
                if saldo > 0:
                    # Crear asiento de cierre para esta cuenta de gasto
                    asiento_cierre = Asiento.objects.create(
                        fecha=fecha_cierre,
                        descripcion=f'Cierre contable {ano_cierre} - {cuenta.nombre}',
                        creado_por=request.user,
                        tiene_iva=False,
                        monto_total=saldo
                    )
                    
                    # Partida 1: Abono a la cuenta de gasto (para cerrarla)
                    Partida.objects.create(
                        asiento=asiento_cierre,
                        cuenta=cuenta,
                        debe=0,
                        haber=saldo,
                        descripcion=f'Cierre de cuenta de gasto {ano_cierre}'
                    )
                    
                    # Partida 2: Cargo a utilidad del ejercicio
                    Partida.objects.create(
                        asiento=asiento_cierre,
                        cuenta=cuenta_utilidad_ejercicio,
                        debe=saldo,
                        haber=0,
                        descripcion=f'Traspaso a utilidad {ano_cierre}'
                    )
            
            # 3. Crear asiento resumen del cierre
            total_asientos = Asiento.objects.filter(
                descripcion__icontains=f'cierre contable {ano_cierre}'
            ).count()
        
        return JsonResponse({
            'success': True,
            'message': f'Cierre contable para el año {ano_cierre} ejecutado exitosamente. Se crearon {total_asientos} asientos de cierre.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al ejecutar el cierre contable: {str(e)}'
        })