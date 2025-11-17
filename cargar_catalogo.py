import os
import django
from django.db import transaction

# --- INICIO DE LA CONFIGURACIÓN DE DJANGO ---
# 1. Especifica la ubicación de tu archivo settings.py
#    (Asume que tu proyecto principal se llama 'Contacloud')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Contacloud.settings')

# 2. Inicializa el entorno de Django
django.setup()
# --- FIN DE LA CONFIGURACIÓN DE DJANGO ---

from contabilidad.models import Cuenta

# DATOS DEL CATÁLOGO COMPLETO
catalogo_completo = [
    # ACTIVO
    {"codigo": "1", "nombre": "ACTIVO", "tipo": "activo", "descripcion": "Grupo principal de activos"},
    {"codigo": "1.1", "nombre": "Activo Corriente", "tipo": "activo", "descripcion": "Activos circulantes"},
    {"codigo": "1.1.1", "nombre": "Caja", "tipo": "activo", "descripcion": "Fondos en efectivo"},
    {"codigo": "1.1.2", "nombre": "Bancos", "tipo": "activo", "descripcion": "Cuentas bancarias"},
    {"codigo": "1.1.3", "nombre": "IVA Credito Fiscal", "tipo": "activo", "descripcion": "IVA acreditable", "acepta_iva": True},
    {"codigo": "1.1.4", "nombre": "Inventario de licencias de software", "tipo": "activo", "descripcion": "Licencias en inventario"},
    {"codigo": "1.1.5", "nombre": "Gastos pagados por anticipado", "tipo": "activo", "descripcion": "Gastos anticipados"},
    
    {"codigo": "1.2", "nombre": "Activo No Corriente", "tipo": "activo", "descripcion": "Activos fijos"},
    {"codigo": "1.2.1", "nombre": "Propiedad planta y equipo", "tipo": "activo", "descripcion": "Activos fijos tangibles"},
    {"codigo": "1.2.1.1", "nombre": "Equipos de computo", "tipo": "activo", "descripcion": "Computadoras y equipos"},
    {"codigo": "1.2.1.2", "nombre": "Mobiliario y Equipo de oficina", "tipo": "activo", "descripcion": "Muebles y equipos de oficina"},
    
    {"codigo": "1.2.2", "nombre": "Activos intangibles", "tipo": "activo", "descripcion": "Activos intangibles"},
    {"codigo": "1.2.2.1", "nombre": "Licencias y derechos de uso", "tipo": "activo", "descripcion": "Licencias de software"},
    {"codigo": "1.2.2.2", "nombre": "Amortización acumulada de intangibles", "tipo": "activo", "descripcion": "Amortización acumulada"},
    {"codigo": "1.2.2.3", "nombre": "Software propio", "tipo": "activo", "descripcion": "Desarrollo de software propio"},

    # PASIVO
    {"codigo": "2", "nombre": "PASIVO", "tipo": "pasivo", "descripcion": "Grupo principal de pasivos"},
    {"codigo": "2.1", "nombre": "Pasivo Corriente", "tipo": "pasivo", "descripcion": "Pasivos a corto plazo"},
    {"codigo": "2.1.1", "nombre": "Proveedores", "tipo": "pasivo", "descripcion": "Cuentas por pagar a proveedores"},
    {"codigo": "2.1.2", "nombre": "Sueldos y prestaciones por pagar", "tipo": "pasivo", "descripcion": "Nomina por pagar"},
    {"codigo": "2.1.3", "nombre": "Impuestos por pagar", "tipo": "pasivo", "descripcion": "Impuestos pendientes de pago"},
    {"codigo": "2.1.4", "nombre": "IVA Debito fiscal", "tipo": "pasivo", "descripcion": "IVA por pagar", "acepta_iva": True},
    {"codigo": "2.1.5", "nombre": "Prestamos a corto plazo", "tipo": "pasivo", "descripcion": "Prestamos corto plazo"},
    
    {"codigo": "2.2", "nombre": "Pasivo No Corriente", "tipo": "pasivo", "descripcion": "Pasivos a largo plazo"},
    {"codigo": "2.2.1", "nombre": "Prestamos bancarios a largo plazo", "tipo": "pasivo", "descripcion": "Prestamos largo plazo"},

    # CAPITAL
    {"codigo": "3", "nombre": "CAPITAL", "tipo": "capital", "descripcion": "Grupo principal de capital"},
    {"codigo": "3.1", "nombre": "Capital Social", "tipo": "capital", "descripcion": "Capital social"},
    {"codigo": "3.1.1", "nombre": "Capital Social", "tipo": "capital", "descripcion": "Capital contable"},
    {"codigo": "3.2", "nombre": "Utilidad del ejercicio", "tipo": "capital", "descripcion": "Utilidades del periodo"},

    # INGRESOS
    {"codigo": "4", "nombre": "INGRESOS", "tipo": "ingreso", "descripcion": "Grupo principal de ingresos"},
    {"codigo": "4.1", "nombre": "Ingresos por Licencias", "tipo": "ingreso", "descripcion": "Venta de licencias"},
    {"codigo": "4.2", "nombre": "Otros Ingresos", "tipo": "ingreso", "descripcion": "Otros ingresos operativos"},

    # COSTOS Y GASTOS
    {"codigo": "5", "nombre": "COSTOS Y GASTOS", "tipo": "gasto", "descripcion": "Grupo principal de costos y gastos"},
    {"codigo": "5.1", "nombre": "Costos", "tipo": "gasto", "descripcion": "Costos directos"},
    {"codigo": "5.1.1", "nombre": "Costo de ventas de licencias digitales", "tipo": "gasto", "descripcion": "Costo de ventas"},
    {"codigo": "5.1.2", "nombre": "Costo de produccion de software", "tipo": "gasto", "descripcion": "Costos de produccion"},
    {"codigo": "5.1.3", "nombre": "Costos indirectos de desarrollo", "tipo": "gasto", "descripcion": "Costos indirectos"},
    
    {"codigo": "5.2", "nombre": "Gastos Operativos", "tipo": "gasto", "descripcion": "Gastos de operación"},
    
    {"codigo": "5.2.1", "nombre": "Gastos Administrativos", "tipo": "gasto", "descripcion": "Gastos administrativos"},
    {"codigo": "5.2.1.1", "nombre": "Sueldos administrativos", "tipo": "gasto", "descripcion": "Sueldos del personal administrativo"},
    {"codigo": "5.2.1.2", "nombre": "Servicios publicos y alquiler de oficinas", "tipo": "gasto", "descripcion": "Pago de servicios y renta"},
    {"codigo": "5.2.1.3", "nombre": "Papelería y suministros", "tipo": "gasto", "descripcion": "Suministros de oficina"},
    {"codigo": "5.2.1.4", "nombre": "Amortizacion de intangibles", "tipo": "gasto", "descripcion": "Gasto por amortización"},

    {"codigo": "5.2.2", "nombre": "Gastos de Ventas", "tipo": "gasto", "descripcion": "Gastos relacionados con la venta"},
    {"codigo": "5.2.2.1", "nombre": "Publicidad y marketing digital", "tipo": "gasto", "descripcion": "Inversión en promoción y ventas"},
    {"codigo": "5.2.2.2", "nombre": "Sueldos de ventas", "tipo": "gasto", "descripcion": "Sueldos del personal de ventas"},
    {"codigo": "5.2.2.3", "nombre": "Comisiones", "tipo": "gasto", "descripcion": "Comisiones a vendedores"},

    {"codigo": "5.2.3", "nombre": "Gastos Financieros", "tipo": "gasto", "descripcion": "Gastos por uso de recursos financieros"},
    {"codigo": "5.2.3.1", "nombre": "Intereses pagados", "tipo": "gasto", "descripcion": "Intereses de préstamos"},
    {"codigo": "5.2.3.2", "nombre": "Gastos bancarios", "tipo": "gasto", "descripcion": "Comisiones y gastos bancarios"},
    {"codigo": "5.2.3.3", "nombre": "Faltante de caja", "tipo": "gasto", "descripcion": "Faltante en arqueo de caja"},
]

print("🔄 INICIANDO CARGA DEL CATÁLOGO...")
print("=" * 50)

# PRIMERO: Verificar cuentas existentes
print("🧹 Verificando cuentas existentes...")
# Asegúrate de que Django esté inicializado antes de llamar a Cuenta.objects.
codigos_existentes = Cuenta.objects.values_list('codigo', flat=True)
print(f"Cuentas existentes en BD: {len(codigos_existentes)}")

cuentas_creadas = 0
cuentas_actualizadas = 0
errores = 0

# --- LÓGICA PARA ASIGNAR CUENTA PADRE Y es_cuenta_detalle ---

def get_cuenta_padre(codigo):
    """Función auxiliar para encontrar el código de la cuenta padre."""
    # Split the code at the last dot, max once.
    partes = codigo.rsplit('.', 1)
    # Returns the parent code if it exists and is not the same as the original code
    return partes[0] if len(partes) > 1 and partes[0] != codigo else None

# Pre-procesar para añadir es_cuenta_detalle y cuenta_padre
for cuenta_data in catalogo_completo:
    # 1. Asigna cuenta_padre (solo el código)
    cuenta_data['cuenta_padre_codigo'] = get_cuenta_padre(cuenta_data['codigo'])
    
    # 2. Define 'es_cuenta_detalle'
    # Si el código tiene 3 o más niveles (ej: 1.1.1 o 1.2.1.1), es cuenta de detalle (True)
    # Si tiene menos de 3 niveles (ej: 1, 1.1), es cuenta de grupo (False)
    # Esto sobrescribe el valor pre-existente si fue definido manualmente en el diccionario
    if cuenta_data['codigo'].count('.') >= 2:
        cuenta_data['es_cuenta_detalle'] = True
    else:
        cuenta_data['es_cuenta_detalle'] = False

# --- INICIO DEL PROCESO DE CARGA EN DOS PASOS ---
with transaction.atomic():
    # PASO 1: Crear/Actualizar las cuentas SIN asignar la Foreign Key (FK) a la cuenta padre
    cuentas_map = {}
    print("\n📝 CREANDO/ACTUALIZANDO CUENTAS (PASO 1: Datos)...")
    for cuenta_data in catalogo_completo:
        codigo = cuenta_data['codigo']
        try:
            # Preparar datos sin la FK del padre aún
            data_to_save = {k: v for k, v in cuenta_data.items() if k not in ['cuenta_padre_codigo', 'grupo']}

            # Buscar por código EXACTO
            cuenta_existente = Cuenta.objects.filter(codigo=codigo).first()
            
            if cuenta_existente:
                # ACTUALIZAR cuenta existente
                for key, value in data_to_save.items():
                    setattr(cuenta_existente, key, value)
                cuenta_existente.save(update_fields=data_to_save.keys())
                cuentas_actualizadas += 1
                # print(f"🔄 ACTUALIZADA (Paso 1): {codigo} - {cuenta_data['nombre']}")
            else:
                # CREAR nueva cuenta
                cuenta_existente = Cuenta.objects.create(**data_to_save)
                cuentas_creadas += 1
                # print(f"✅ CREADA (Paso 1): {codigo} - {cuenta_data['nombre']}")
            
            # Mapear la instancia para el Paso 2
            cuentas_map[codigo] = cuenta_existente
            
        except Exception as e:
            errores += 1
            print(f"❌ ERROR (Paso 1) en {codigo}: {str(e)}")

    # PASO 2: Asignar la Foreign Key (FK) de la cuenta padre usando las instancias creadas
    print("\n🔗 ASIGNANDO CUENTAS PADRES (PASO 2: Enlaces FK)...")
    for cuenta_data in catalogo_completo:
        codigo = cuenta_data['codigo']
        cuenta_padre_codigo = cuenta_data.get('cuenta_padre_codigo')
        
        if cuenta_padre_codigo:
            try:
                hija = cuentas_map.get(codigo)
                padre = cuentas_map.get(cuenta_padre_codigo)
                
                if hija and padre and hija.cuenta_padre != padre:
                    hija.cuenta_padre = padre
                    hija.save(update_fields=['cuenta_padre'])
                    # print(f"   -> Enlazada: {codigo} a {cuenta_padre_codigo}")
                
            except Exception as e:
                errores += 1
                print(f"❌ ERROR (Paso 2) en enlace {codigo} a {cuenta_padre_codigo}: {str(e)}")


print("=" * 50)
print("🎯 RESUMEN FINAL:")
print(f"✅ Cuentas CREADAS: {cuentas_creadas}")
print(f"🔄 Cuentas ACTUALIZADAS: {cuentas_actualizadas}")
print(f"❌ ERRORES: {errores}")
print(f"📊 TOTAL en BD: {Cuenta.objects.count()}")