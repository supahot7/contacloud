# signals.py - VERSIÓN FINAL CORREGIDA (usa costo_unitario)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Partida, Licencia
from django.db import transaction
import re

# signals.py - CORREGIR
@receiver(post_save, sender=Partida)
def actualizar_inventario_licencias(sender, instance, created, **kwargs):
    """
    Señal que se activa cuando se crea una partida contable
    y actualiza el inventario de licencias si corresponde
    """
    if not created:
        return
    
    # Buscar si esta partida está relacionada con venta de licencias
    descripcion = instance.descripcion.lower() if instance.descripcion else ''
    cuenta_nombre = instance.cuenta.nombre.lower()
    cuenta_codigo = instance.cuenta.codigo.lower()
    
    # Palabras clave mejoradas para detectar ventas de licencias
    palabras_clave_venta = [
        'licencia', 'software', 'venta licencia', 'venta software',
        'licencia vendida', 'venta de licencia', 'ingreso por licencia',
        'licencias', 'software vendido', 'venta de software', 'ingreso licencia'
    ]
    
    # Cuentas específicas de ingresos por licencias (códigos y nombres)
    cuentas_ingreso_licencias = [
        'ingresos por licencias',
        'ingreso por licencias',
        'venta de licencias',
        'ingresos licencias',
        '4.1',  # Código típico para ingresos por servicios/licencias
        '41'    # Código alternativo
    ]
    
    # Verificar si es una venta de licencias (en el HABER para ingresos)
    es_venta_licencia = (
        any(palabra in descripcion for palabra in palabras_clave_venta) or
        any(cuenta in cuenta_nombre for cuenta in cuentas_ingreso_licencias) or
        any(codigo in cuenta_codigo for codigo in ['4.1', '41'])
    ) and instance.haber > 0  # Los ingresos van en el HABER
    
    if es_venta_licencia:
        try:
            with transaction.atomic():
                print(f"🔍 Detectada posible venta de licencia: {descripcion} - Monto: {instance.haber}")
                
                # Buscar todas las licencias disponibles
                licencias = Licencia.objects.filter(
                    estado='disponible',
                    cantidad_disponible__gt=0
                ).order_by('-creado_en')
                
                if not licencias.exists():
                    print("⚠️ No hay licencias disponibles en inventario")
                    return
                
                # Intentar encontrar la licencia específica por descripción
                licencia_encontrada = None
                
                # Buscar por nombre o código en la descripción
                for licencia in licencias:
                    if (licencia.nombre.lower() in descripcion or 
                        licencia.codigo.lower() in descripcion):
                        licencia_encontrada = licencia
                        print(f"✅ Licencia específica encontrada: {licencia_encontrada.nombre}")
                        break
                
                # Si no se encuentra específica, usar la más reciente
                if not licencia_encontrada:
                    licencia_encontrada = licencias.first()
                    print(f"⚠️ Usando licencia más reciente: {licencia_encontrada.nombre}")
                
                # Determinar la cantidad vendida
                cantidad_vendida = 1  # Por defecto 1 licencia
                
                # 1. Primero intentar extraer de la descripción
                match = re.search(r'(\d+)\s*licencia', descripcion)
                if match:
                    cantidad_vendida = int(match.group(1))
                    print(f"📊 Cantidad extraída de descripción: {cantidad_vendida}")
                # 2. Si no se especifica, calcular basado en costo_unitario
                elif licencia_encontrada.costo_unitario > 0:
                    monto_venta = instance.haber
                    cantidad_calculada = monto_venta / licencia_encontrada.costo_unitario
                    # Redondear al entero más cercano
                    cantidad_vendida = max(1, round(cantidad_calculada))
                    print(f"📊 Cantidad calculada: {cantidad_vendida} (Monto: ${monto_venta} / Costo: ${licencia_encontrada.costo_unitario})")
                
                # Validar y ejecutar la venta
                if cantidad_vendida > 0:
                    if cantidad_vendida <= licencia_encontrada.cantidad_disponible:
                        # ✅ CORREGIDO: Usar el nombre correcto del método
                        licencia_encontrada.vender_licencia(cantidad_vendida)
                        print(f"✅ Inventario actualizado: {cantidad_vendida} licencia(s) vendida(s) de {licencia_encontrada.nombre}")
                        print(f"📊 Nuevo stock: {licencia_encontrada.cantidad_disponible}")
                        
                        # Opcional: Actualizar la descripción de la partida
                        if not instance.descripcion:
                            instance.descripcion = ""
                        info_licencia = f" - Licencia: {licencia_encontrada.nombre} (x{cantidad_vendida})"
                        if info_licencia not in instance.descripcion:
                            instance.descripcion += info_licencia
                            instance.save(update_fields=['descripcion'])
                    else:
                        print(f"❌ Stock insuficiente. Se requieren {cantidad_vendida}, disponibles: {licencia_encontrada.cantidad_disponible}")
                else:
                    print("⚠️ Cantidad vendida no válida")
                    
        except Exception as e:
            print(f"❌ Error actualizando inventario: {str(e)}")
            import traceback
            print(f"🔍 Traceback: {traceback.format_exc()}")