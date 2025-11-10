from django.core.management.base import BaseCommand
from contabilidad.models import Cuenta

class Command(BaseCommand):
    help = 'Crea el catálogo de cuentas inicial para ContaCloud según el documento'

    def handle(self, *args, **options):
        cuentas = [
            # ===== ACTIVO =====
            {'codigo': '1', 'nombre': 'ACTIVO', 'tipo': 'activo', 'grupo': '1', 'es_cuenta_detalle': False},
            
            # Activo Corriente
            {'codigo': '1.1', 'nombre': 'ACTIVO CORRIENTE', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': False},
            {'codigo': '1.1.1', 'nombre': 'Caja', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': True},
            {'codigo': '1.1.2', 'nombre': 'Bancos', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': True},
            {'codigo': '1.1.3', 'nombre': 'IVA Crédito Fiscal', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': True},
            {'codigo': '1.1.4', 'nombre': 'Inventario de licencias de software', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': True},
            {'codigo': '1.1.5', 'nombre': 'Gastos pagados por anticipado', 'tipo': 'activo', 'grupo': '1.1', 'es_cuenta_detalle': True},
            
            # Activo No Corriente
            {'codigo': '1.2', 'nombre': 'ACTIVO NO CORRIENTE', 'tipo': 'activo', 'grupo': '1.2', 'es_cuenta_detalle': False},
            
            # Propiedad planta y equipo
            {'codigo': '1.2.1', 'nombre': 'PROPIEDAD PLANTA Y EQUIPO', 'tipo': 'activo', 'grupo': '1.2.1', 'es_cuenta_detalle': False},
            {'codigo': '1.2.1.1', 'nombre': 'Equipos de cómputo', 'tipo': 'activo', 'grupo': '1.2.1', 'es_cuenta_detalle': True},
            {'codigo': '1.2.1.2', 'nombre': 'Mobiliario y Equipo de oficina', 'tipo': 'activo', 'grupo': '1.2.1', 'es_cuenta_detalle': True},
            
            # Activos intangibles
            {'codigo': '1.2.2', 'nombre': 'ACTIVOS INTANGIBLES', 'tipo': 'activo', 'grupo': '1.2.2', 'es_cuenta_detalle': False},
            {'codigo': '1.2.2.1', 'nombre': 'Licencias y derechos de uso', 'tipo': 'activo', 'grupo': '1.2.2', 'es_cuenta_detalle': True},
            {'codigo': '1.2.2.2', 'nombre': 'Amortización acumulada de intangibles', 'tipo': 'activo', 'grupo': '1.2.2', 'es_cuenta_detalle': True},
            {'codigo': '1.2.2.3', 'nombre': 'Software propio', 'tipo': 'activo', 'grupo': '1.2.2', 'es_cuenta_detalle': True},
            
            # ===== PASIVO =====
            {'codigo': '2', 'nombre': 'PASIVO', 'tipo': 'pasivo', 'grupo': '2', 'es_cuenta_detalle': False},
            
            # Pasivo Corriente
            {'codigo': '2.1', 'nombre': 'PASIVO CORRIENTE', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': False},
            {'codigo': '2.1.1', 'nombre': 'Proveedores', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': True},
            {'codigo': '2.1.2', 'nombre': 'Sueldos y prestaciones por pagar', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': True},
            {'codigo': '2.1.3', 'nombre': 'Impuestos por pagar', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': True},
            {'codigo': '2.1.4', 'nombre': 'IVA Débito fiscal', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': True},
            {'codigo': '2.1.5', 'nombre': 'Préstamos a corto plazo', 'tipo': 'pasivo', 'grupo': '2.1', 'es_cuenta_detalle': True},
            
            # Pasivo No Corriente
            {'codigo': '2.2', 'nombre': 'PASIVO NO CORRIENTE', 'tipo': 'pasivo', 'grupo': '2.2', 'es_cuenta_detalle': False},
            {'codigo': '2.2.1', 'nombre': 'Préstamos bancarios a largo plazo', 'tipo': 'pasivo', 'grupo': '2.2', 'es_cuenta_detalle': True},
            
            # ===== CAPITAL =====
            {'codigo': '3', 'nombre': 'CAPITAL', 'tipo': 'capital', 'grupo': '3', 'es_cuenta_detalle': False},
            
            # Capital Social
            {'codigo': '3.1', 'nombre': 'CAPITAL SOCIAL', 'tipo': 'capital', 'grupo': '3.1', 'es_cuenta_detalle': False},
            {'codigo': '3.1.1', 'nombre': 'Capital Social', 'tipo': 'capital', 'grupo': '3.1', 'es_cuenta_detalle': True},
            {'codigo': '3.2', 'nombre': 'Utilidad del ejercicio', 'tipo': 'capital', 'grupo': '3.2', 'es_cuenta_detalle': True},
            
            # ===== INGRESOS =====
            {'codigo': '4', 'nombre': 'INGRESOS', 'tipo': 'ingreso', 'grupo': '4', 'es_cuenta_detalle': False},
            {'codigo': '4.1', 'nombre': 'Ingresos por Licencias', 'tipo': 'ingreso', 'grupo': '4.1', 'es_cuenta_detalle': True},
            {'codigo': '4.2', 'nombre': 'Otros Ingresos', 'tipo': 'ingreso', 'grupo': '4.2', 'es_cuenta_detalle': True},
            
            # ===== GASTOS =====
            {'codigo': '5', 'nombre': 'GASTOS', 'tipo': 'gasto', 'grupo': '5', 'es_cuenta_detalle': False},
            
            # Costos
            {'codigo': '5.1', 'nombre': 'COSTOS', 'tipo': 'gasto', 'grupo': '5.1', 'es_cuenta_detalle': False},
            {'codigo': '5.1.1', 'nombre': 'Costo de ventas de licencias digitales', 'tipo': 'gasto', 'grupo': '5.1', 'es_cuenta_detalle': True},
            {'codigo': '5.1.2', 'nombre': 'Costo de producción de software', 'tipo': 'gasto', 'grupo': '5.1', 'es_cuenta_detalle': True},
            {'codigo': '5.1.3', 'nombre': 'Costos indirectos de desarrollo', 'tipo': 'gasto', 'grupo': '5.1', 'es_cuenta_detalle': True},
            
            # Gastos Operativos
            {'codigo': '5.2', 'nombre': 'GASTOS OPERATIVOS', 'tipo': 'gasto', 'grupo': '5.2', 'es_cuenta_detalle': False},
            
            # Gastos Administrativos
            {'codigo': '5.2.1', 'nombre': 'GASTOS ADMINISTRATIVOS', 'tipo': 'gasto', 'grupo': '5.2.1', 'es_cuenta_detalle': False},
            {'codigo': '5.2.1.1', 'nombre': 'Sueldos administrativos', 'tipo': 'gasto', 'grupo': '5.2.1', 'es_cuenta_detalle': True},
            {'codigo': '5.2.1.2', 'nombre': 'Servicios públicos y alquiler de oficinas', 'tipo': 'gasto', 'grupo': '5.2.1', 'es_cuenta_detalle': True},
            {'codigo': '5.2.1.3', 'nombre': 'Papelería y suministros', 'tipo': 'gasto', 'grupo': '5.2.1', 'es_cuenta_detalle': True},
            {'codigo': '5.2.1.4', 'nombre': 'Amortización de intangibles', 'tipo': 'gasto', 'grupo': '5.2.1', 'es_cuenta_detalle': True},
            
            # Gastos de Ventas
            {'codigo': '5.2.2', 'nombre': 'GASTOS DE VENTAS', 'tipo': 'gasto', 'grupo': '5.2.2', 'es_cuenta_detalle': False},
            {'codigo': '5.2.2.1', 'nombre': 'Publicidad y marketing digital', 'tipo': 'gasto', 'grupo': '5.2.2', 'es_cuenta_detalle': True},
            
            # Gastos Financieros
            {'codigo': '5.2.3', 'nombre': 'GASTOS FINANCIEROS', 'tipo': 'gasto', 'grupo': '5.2.3', 'es_cuenta_detalle': False},
            {'codigo': '5.2.3.1', 'nombre': 'Intereses pagados', 'tipo': 'gasto', 'grupo': '5.2.3', 'es_cuenta_detalle': True},
            {'codigo': '5.2.3.2', 'nombre': 'Gastos bancarios', 'tipo': 'gasto', 'grupo': '5.2.3', 'es_cuenta_detalle': True},
            {'codigo': '5.2.3.3', 'nombre': 'Faltante de caja', 'tipo': 'gasto', 'grupo': '5.2.3', 'es_cuenta_detalle': True},
        ]
        
        cuentas_creadas = 0
        cuentas_actualizadas = 0
        
        # PRIMERO: Limpiar cuentas existentes si es la primera ejecución
        if Cuenta.objects.count() > 0:
            self.stdout.write(self.style.WARNING('⚠️ Ya existen cuentas en la base de datos.'))
            self.stdout.write('📝 Se actualizarán las cuentas existentes en lugar de crear duplicados.')
        
        for cuenta_data in cuentas:
            # Buscar cuenta padre basado en el código
            codigo_padre = '.'.join(cuenta_data['codigo'].split('.')[:-1])
            cuenta_padre = None
            if codigo_padre:
                try:
                    cuenta_padre = Cuenta.objects.get(codigo=codigo_padre)
                except Cuenta.DoesNotExist:
                    # Si no existe el padre, continuar igual (se creará después)
                    pass
            
            # Usar update_or_create para evitar duplicados
            cuenta, created = Cuenta.objects.update_or_create(
                codigo=cuenta_data['codigo'],
                defaults={
                    'nombre': cuenta_data['nombre'],
                    'tipo': cuenta_data['tipo'],
                    'grupo': cuenta_data['grupo'],
                    'es_cuenta_detalle': cuenta_data['es_cuenta_detalle'],
                    'cuenta_padre': cuenta_padre,
                    'descripcion': f"Cuenta de {cuenta_data['tipo']}"
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Cuenta creada: {cuenta.codigo} - {cuenta.nombre}'))
                cuentas_creadas += 1
            else:
                self.stdout.write(self.style.WARNING(f'🔄 Cuenta actualizada: {cuenta.codigo} - {cuenta.nombre}'))
                cuentas_actualizadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 ¡Proceso completado!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Cuentas creadas: {cuentas_creadas}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Cuentas actualizadas: {cuentas_actualizadas}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total de cuentas en el sistema: {Cuenta.objects.count()}'))