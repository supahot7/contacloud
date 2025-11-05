# costos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ManoObra,CostoIndirecto,Planilla
from decimal import Decimal

def mano_obra(request):
    """Vista para la gestión de mano de obra"""
    
    # Obtener registros de Mano de Obra
    registros_mo = ManoObra.objects.all().order_by('-creado_en')
    total_mod = sum([reg.costo_mensual for reg in registros_mo]) if registros_mo else 0
    
    # Obtener registros de Costos Indirectos (para que funcionen los otros tabs)
    registros_cif = CostoIndirecto.objects.all().order_by('-creado_en')
    total_cif = sum([reg.monto for reg in registros_cif]) if registros_cif else 0
    
    # Calcular tasa CIF
    tasa_cif = (total_cif / total_mod * 100) if total_mod > 0 else 0
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre_trabajador')
            cargo = request.POST.get('cargo')
            costo = request.POST.get('costo_mensual')
            fecha = request.POST.get('fecha_mo')
            observaciones = request.POST.get('observaciones_mo', '')
            tipo_contrato = request.POST.get('tipo_contrato', 'tiempo_completo')
            
            if not all([nombre, cargo, costo, fecha]):
                messages.error(request, 'Todos los campos marcados como requeridos deben ser completados.')
                return redirect('costos:manoObra')
            
            if Decimal(costo) <= 0:
                messages.error(request, 'El costo mensual debe ser mayor a cero.')
                return redirect('costos:manoObra')
            
            ManoObra.objects.create(
                nombre_trabajador=nombre,
                cargo=cargo,
                costo_mensual=Decimal(costo),
                fecha_registro=fecha,
                observaciones=observaciones,
                tipo_contrato=tipo_contrato,
                usuario='usuario_temporal'
            )
            
            messages.success(request, f'Registro de {nombre} agregado correctamente.')
            return redirect('costos:manoObra')
            
        except Exception as e:
            messages.error(request, f'Error al guardar el registro: {str(e)}')
    
    # Contexto COMPLETO para todos los tabs
    context = {
        'registros_mo': registros_mo,
        'total_mod': total_mod,
        'registros_cif': registros_cif,
        'total_cif': total_cif,
        'tasa_cif': tasa_cif
    }
    return render(request, 'costos/manoObra.html', context)

def costos_indirectos(request):
    """Vista para la gestión de costos indirectos"""
    
    # Obtener registros de Costos Indirectos
    registros_cif = CostoIndirecto.objects.all().order_by('-creado_en')
    total_cif = sum([reg.monto for reg in registros_cif]) if registros_cif else 0
    
    # Obtener registros de Mano de Obra (para que funcionen los otros tabs)
    registros_mo = ManoObra.objects.all().order_by('-creado_en')
    total_mod = sum([reg.costo_mensual for reg in registros_mo]) if registros_mo else 0
    
    # Calcular tasa CIF
    tasa_cif = (total_cif / total_mod * 100) if total_mod > 0 else 0
    
    if request.method == 'POST':
        try:
            concepto = request.POST.get('concepto')
            categoria = request.POST.get('categoria')
            monto = request.POST.get('monto')
            fecha = request.POST.get('fecha_cif')
            descripcion = request.POST.get('descripcion', '')
            
            if not all([concepto, categoria, monto, fecha]):
                messages.error(request, 'Todos los campos marcados como requeridos deben ser completados.')
                return redirect('costos:costosIndirectos')
            
            if Decimal(monto) <= 0:
                messages.error(request, 'El monto debe ser mayor a cero.')
                return redirect('costos:costosIndirectos')
            
            CostoIndirecto.objects.create(
                concepto=concepto,
                categoria=categoria,
                monto=Decimal(monto),
                fecha_registro=fecha,
                descripcion=descripcion,
                usuario='usuario_temporal'
            )
            
            messages.success(request, f'Costo indirecto "{concepto}" agregado correctamente.')
            return redirect('costos:costosIndirectos')
            
        except Exception as e:
            messages.error(request, f'Error al guardar el registro: {str(e)}')
    
    # Contexto COMPLETO para todos los tabs
    context = {
        'registros_mo': registros_mo,
        'total_mod': total_mod,
        'registros_cif': registros_cif,
        'total_cif': total_cif,
        'tasa_cif': tasa_cif
    }
    return render(request, 'costos/manoObra.html', context)

def eliminar_mano_obra(request, id):
    """Vista para eliminar registro de mano de obra"""
    if request.method == 'POST':
        try:
            registro = get_object_or_404(ManoObra, id=id)
            nombre = registro.nombre_trabajador
            registro.delete()
            messages.success(request, f'Registro de {nombre} eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el registro: {str(e)}')
    
    return redirect('costos:manoObra')

def eliminar_costo_indirecto(request, id):
    """Vista para eliminar registro de costo indirecto"""
    if request.method == 'POST':
        try:
            registro = get_object_or_404(CostoIndirecto, id=id)
            concepto = registro.concepto
            registro.delete()
            messages.success(request, f'Costo indirecto "{concepto}" eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el registro: {str(e)}')
    
    return redirect('costos:costosIndirectos')


def planilla(request):
    """Vista para el cálculo de planilla con cálculos corregidos"""
    if request.method == 'POST':
        try:
            # Procesar el formulario de planilla
            nombre_empleado = request.POST.get('nombre_empleado')
            puesto = request.POST.get('puesto')
            salario_nominal = request.POST.get('salario_nominal')
            dias_trabajados = request.POST.get('dias_trabajados')
            anos_trabajados = request.POST.get('anos_trabajados')
            
            # Validaciones
            if not all([nombre_empleado, puesto, salario_nominal, dias_trabajados, anos_trabajados]):
                messages.error(request, 'Todos los campos marcados como requeridos deben ser completados.')
                return redirect('costos:planilla')
            
            if Decimal(salario_nominal) <= 0:
                messages.error(request, 'El salario nominal debe ser mayor a cero.')
                return redirect('costos:planilla')
            
            if int(dias_trabajados) <= 0 or int(dias_trabajados) > 31:
                messages.error(request, 'Los días trabajados deben estar entre 1 y 31.')
                return redirect('costos:planilla')
            
            # Mapear nombres del formulario a los valores del modelo
            nombre_map = {
                'Juan Pérez': 'juan_perez',
                'María García': 'maria_garcia', 
                'Carlos López': 'carlos_lopez',
                'Ana Martínez': 'ana_martinez'
            }
            
            puesto_map = {
                'Contador': 'contador',
                'Operario': 'operario',
                'Supervisor': 'supervisor',
                'Gerente': 'gerente',
                'Asistente': 'asistente'
            }
            
            # Crear registro en planilla
            planilla_obj = Planilla(
                nombre=nombre_map.get(nombre_empleado, 'juan_perez'),
                puesto=puesto_map.get(puesto, 'contador'),
                salario_nominal_mensual=Decimal(salario_nominal),
                dias_trabajados=int(dias_trabajados),
                antiguedad=anos_trabajados,
                usuario=request.user.username if request.user.is_authenticated else 'usuario_temporal'
            )
            
            # Los cálculos se hacen automáticamente en save() con el método calcular_totales()
            planilla_obj.save()
            
            messages.success(request, f'Empleado {nombre_empleado} agregado a la planilla correctamente.')
            return redirect('costos:planilla')
            
        except Exception as e:
            messages.error(request, f'Error al guardar en planilla: {str(e)}')
    
    # Obtener registros existentes para mostrar en la tabla
    registros_planilla = Planilla.objects.all().order_by('-creado_en')
    
    # Calcular totales para la tabla
    total_semanal = sum(reg.salario_total_semanal for reg in registros_planilla)
    total_mensual = sum(reg.salario_total_mensual for reg in registros_planilla)
    
    context = {
        'registros_planilla': registros_planilla,
        'total_semanal': total_semanal,
        'total_mensual': total_mensual
    }
    return render(request, 'costos/planilla.html', context)

def eliminar_registro_planilla(request, id):
    """Vista para eliminar registro de planilla"""
    if request.method == 'POST':
        try:
            registro = get_object_or_404(Planilla, id=id)
            nombre = registro.get_nombre_display()
            registro.delete()
            messages.success(request, f'Registro de {nombre} eliminado correctamente de la planilla.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el registro: {str(e)}')
    
    return redirect('costos:planilla')
def calcular_planilla_ajax(request):
    """Vista para cálculo en tiempo real (AJAX)"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            salario_nominal = Decimal(request.POST.get('salario_nominal', 0))
            anos_trabajados = request.POST.get('anos_trabajados', '1-3')
            dias_trabajados = int(request.POST.get('dias_trabajados', 30))  # ✅ OBTENER DÍAS TRABAJADOS
            
            # Validar días trabajados
            if dias_trabajados <= 0 or dias_trabajados > 31:
                return JsonResponse({'success': False, 'error': 'Días trabajados inválidos'})
            
            # Crear objeto temporal para los cálculos
            planilla_temp = Planilla(
                salario_nominal_mensual=salario_nominal,
                antiguedad=anos_trabajados,
                dias_trabajados=dias_trabajados  # ✅ USAR LOS DÍAS TRABAJADOS
            )
            planilla_temp.calcular_totales()
            
            # Devolver resultados en JSON
            return JsonResponse({
                'sueldo_nominal': float(planilla_temp.sueldo_nominal),
                'costo_semana': float(planilla_temp.costo_semana_salarial),
                'septimo': float(planilla_temp.septimo),
                'vacaciones': float(planilla_temp.vacaciones),
                'aguinaldo': float(planilla_temp.aguinaldo),
                'salario_cancelado': float(planilla_temp.calculo_salario_cancelado),
                'isss': float(planilla_temp.isss),
                'afp': float(planilla_temp.afp),
                'incaf': float(planilla_temp.incaf),
                'total_semanal': float(planilla_temp.salario_total_semanal),
                'total_mensual': float(planilla_temp.salario_total_mensual),
                'success': True
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})