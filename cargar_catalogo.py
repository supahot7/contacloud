from contabilidad.models import Cuenta

# DATOS DEL CATÁLOGO COMPLETO
catalogo_completo = [
    # ACTIVO
    {"codigo": "1", "nombre": "ACTIVO", "tipo": "activo", "grupo": "1", "descripcion": "Grupo principal de activos"},
    {"codigo": "1.1", "nombre": "Activo Corriente", "tipo": "activo", "grupo": "1.1", "descripcion": "Activos circulantes"},
    {"codigo": "1.1.1", "nombre": "Caja", "tipo": "activo", "grupo": "1.1.1", "descripcion": "Fondos en efectivo"},
    {"codigo": "1.1.2", "nombre": "Bancos", "tipo": "activo", "grupo": "1.1.2", "descripcion": "Cuentas bancarias"},
    {"codigo": "1.1.3", "nombre": "IVA Crédito Fiscal", "tipo": "activo", "grupo": "1.1.3", "descripcion": "IVA acreditable"},
    {"codigo": "1.1.4", "nombre": "Inventario de licencias de software", "tipo": "activo", "grupo": "1.1.4", "descripcion": "Licencias en inventario"},
    {"codigo": "1.1.5", "nombre": "Gastos pagados por anticipado", "tipo": "activo", "grupo": "1.1.5", "descripcion": "Gastos anticipados"},
    
    {"codigo": "1.2", "nombre": "Activo No Corriente", "tipo": "activo", "grupo": "1.2", "descripcion": "Activos fijos"},
    {"codigo": "1.2.1", "nombre": "Propiedad planta y equipo", "tipo": "activo", "grupo": "1.2.1", "descripcion": "Activos fijos tangibles"},
    {"codigo": "1.2.1.1", "nombre": "Equipos de cómputo", "tipo": "activo", "grupo": "1.2.1.1", "descripcion": "Computadoras y equipos"},
    {"codigo": "1.2.1.2", "nombre": "Mobiliario y Equipo de oficina", "tipo": "activo", "grupo": "1.2.1.2", "descripcion": "Muebles y equipos de oficina"},
    
    {"codigo": "1.2.2", "nombre": "Activos intangibles", "tipo": "activo", "grupo": "1.2.2", "descripcion": "Activos intangibles"},
    {"codigo": "1.2.2.1", "nombre": "Licencias y derechos de uso", "tipo": "activo", "grupo": "1.2.2.1", "descripcion": "Licencias de software"},
    {"codigo": "1.2.2.2", "nombre": "Amortización acumulada de intangibles", "tipo": "activo", "grupo": "1.2.2.2", "descripcion": "Amortización acumulada"},
    {"codigo": "1.2.2.3", "nombre": "Software propio", "tipo": "activo", "grupo": "1.2.2.3", "descripcion": "Desarrollo de software propio"},

    # PASIVO
    {"codigo": "2", "nombre": "PASIVO", "tipo": "pasivo", "grupo": "2", "descripcion": "Grupo principal de pasivos"},
    {"codigo": "2.1", "nombre": "Pasivo Corriente", "tipo": "pasivo", "grupo": "2.1", "descripcion": "Pasivos a corto plazo"},
    {"codigo": "2.1.1", "nombre": "Proveedores", "tipo": "pasivo", "grupo": "2.1.1", "descripcion": "Cuentas por pagar a proveedores"},
    {"codigo": "2.1.2", "nombre": "Sueldos y prestaciones por pagar", "tipo": "pasivo", "grupo": "2.1.2", "descripcion": "Nómina por pagar"},
    {"codigo": "2.1.3", "nombre": "Impuestos por pagar", "tipo": "pasivo", "grupo": "2.1.3", "descripcion": "Impuestos pendientes de pago"},
    {"codigo": "2.1.4", "nombre": "IVA Débito fiscal", "tipo": "pasivo", "grupo": "2.1.4", "descripcion": "IVA por pagar"},
    {"codigo": "2.1.5", "nombre": "Préstamos a corto plazo", "tipo": "pasivo", "grupo": "2.1.5", "descripcion": "Préstamos corto plazo"},
    
    {"codigo": "2.2", "nombre": "Pasivo No Corriente", "tipo": "pasivo", "grupo": "2.2", "descripcion": "Pasivos a largo plazo"},
    {"codigo": "2.2.1", "nombre": "Préstamos bancarios a largo plazo", "tipo": "pasivo", "grupo": "2.2.1", "descripcion": "Préstamos largo plazo"},

    # CAPITAL
    {"codigo": "3", "nombre": "CAPITAL", "tipo": "capital", "grupo": "3", "descripcion": "Grupo principal de capital"},
    {"codigo": "3.1", "nombre": "Capital Social", "tipo": "capital", "grupo": "3.1", "descripcion": "Capital social"},
    {"codigo": "3.1.1", "nombre": "Capital Social", "tipo": "capital", "grupo": "3.1.1", "descripcion": "Capital contable"},
    {"codigo": "3.2", "nombre": "Utilidad del ejercicio", "tipo": "capital", "grupo": "3.2", "descripcion": "Utilidades del período"},

    # INGRESOS (Nota: en tu modelo es 'ingreso' no 'ingresos')
    {"codigo": "4", "nombre": "INGRESOS", "tipo": "ingreso", "grupo": "4", "descripcion": "Grupo principal de ingresos"},
    {"codigo": "4.1", "nombre": "Ingresos por Licencias", "tipo": "ingreso", "grupo": "4.1", "descripcion": "Venta de licencias"},
    {"codigo": "4.2", "nombre": "Otros Ingresos", "tipo": "ingreso", "grupo": "4.2", "descripcion": "Otros ingresos operativos"},

    # COSTOS Y GASTOS (Nota: en tu modelo es 'gasto' no 'costos_gastos')
    {"codigo": "5", "nombre": "COSTOS Y GASTOS", "tipo": "gasto", "grupo": "5", "descripcion": "Grupo principal de costos y gastos"},
    {"codigo": "5.1", "nombre": "Costos", "tipo": "gasto", "grupo": "5.1", "descripcion": "Costos directos"},
    {"codigo": "5.1.1", "nombre": "Costo de ventas de licencias digitales", "tipo": "gasto", "grupo": "5.1.1", "descripcion": "Costo de ventas"},
    {"codigo": "5.1.2", "nombre": "Costo de producción de software", "tipo": "gasto", "grupo": "5.1.2", "descripcion": "Costos de producción"},
    {"codigo": "5.1.3", "nombre": "Costos indirectos de desarrollo", "tipo": "gasto", "grupo": "5.1.3", "descripcion": "Costos indirectos"},
    
    {"codigo": "5.2", "nombre": "Gastos Operativos", "tipo": "gasto", "grupo": "5.2", "descripcion": "Gastos de operación"},
    {"codigo": "5.2.1", "nombre": "Gastos Administrativos", "tipo": "gasto", "grupo": "5.2.1", "descripcion": "Gastos administrativos"},
    {"codigo": "5.2.1.1", "nombre": "Sueldos administrativos", "tipo": "gasto", "grupo": "5.2.1.1", "descripcion": "Sueldos del personal administrativo"},
]

print("🔄 INICIANDO CARGA DEL CATÁLOGO...")
print("=" * 50)

# PRIMERO: Verificar cuentas existentes
print("🧹 Verificando cuentas existentes...")
codigos_existentes = Cuenta.objects.values_list('codigo', flat=True)
print(f"Cuentas existentes en BD: {len(codigos_existentes)}")

cuentas_creadas = 0
cuentas_actualizadas = 0
errores = 0

for cuenta_data in catalogo_completo:
    try:
        # Buscar por código EXACTO
        cuenta_existente = Cuenta.objects.filter(codigo=cuenta_data['codigo']).first()
        
        if cuenta_existente:
            # ACTUALIZAR cuenta existente
            for key, value in cuenta_data.items():
                setattr(cuenta_existente, key, value)
            cuenta_existente.save()
            cuentas_actualizadas += 1
            print(f"🔄 ACTUALIZADA: {cuenta_data['codigo']} - {cuenta_data['nombre']}")
        else:
            # CREAR nueva cuenta
            Cuenta.objects.create(**cuenta_data)
            cuentas_creadas += 1
            print(f"✅ CREADA: {cuenta_data['codigo']} - {cuenta_data['nombre']}")
            
    except Exception as e:
        errores += 1
        print(f"❌ ERROR en {cuenta_data['codigo']}: {str(e)}")

print("=" * 50)
print("🎯 RESUMEN FINAL:")
print(f"✅ Cuentas CREADAS: {cuentas_creadas}")
print(f"🔄 Cuentas ACTUALIZADAS: {cuentas_actualizadas}")
print(f"❌ ERRORES: {errores}")
print(f"📊 TOTAL en BD: {Cuenta.objects.count()}")