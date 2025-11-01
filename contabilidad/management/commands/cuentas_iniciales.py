from django.core.management.base import BaseCommand
from contabilidad.models import Cuenta

class Command(BaseCommand):
    help = 'Crea el catálogo de cuentas inicial para ContaCloud según el documento'

    def handle(self, *args, **options):
        cuentas = [
            # ===== ACTIVO =====
            {'codigo': '1', 'nombre': 'ACTIVO', 'tipo': 'ACTIVO', 'es_cuenta_detalle': False},
            
            # Activo Corriente
            {'codigo': '1.1', 'nombre': 'ACTIVO CORRIENTE', 'tipo': 'ACTIVO', 'es_cuenta_detalle': False},
            {'codigo': '1.1.1', 'nombre': 'Caja', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.1.2', 'nombre': 'Bancos', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.1.3', 'nombre': 'IVA Crédito Fiscal', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.1.4', 'nombre': 'Inventario de licencias de software', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.1.5', 'nombre': 'Gastos pagados por anticipado', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            
            # Activo No Corriente
            {'codigo': '1.2', 'nombre': 'ACTIVO NO CORRIENTE', 'tipo': 'ACTIVO', 'es_cuenta_detalle': False},
            
            # Propiedad planta y equipo
            {'codigo': '1.2.1', 'nombre': 'PROPIEDAD PLANTA Y EQUIPO', 'tipo': 'ACTIVO', 'es_cuenta_detalle': False},
            {'codigo': '1.2.1.1', 'nombre': 'Equipos de cómputo', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.2.1.2', 'nombre': 'Mobiliario y Equipo de oficina', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            
            # Activos intangibles
            {'codigo': '1.2.2', 'nombre': 'ACTIVOS INTANGIBLES', 'tipo': 'ACTIVO', 'es_cuenta_detalle': False},
            {'codigo': '1.2.2.2', 'nombre': 'Licencias y derechos de uso', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.2.2.3', 'nombre': 'Amortización acumulada de intangibles', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            {'codigo': '1.2.1.4', 'nombre': 'Software propio', 'tipo': 'ACTIVO', 'es_cuenta_detalle': True},
            
            # ===== PASIVO =====
            {'codigo': '2', 'nombre': 'PASIVO', 'tipo': 'PASIVO', 'es_cuenta_detalle': False},
            
            # Pasivo Corriente
            {'codigo': '2.1', 'nombre': 'PASIVO CORRIENTE', 'tipo': 'PASIVO', 'es_cuenta_detalle': False},
            {'codigo': '2.1.1', 'nombre': 'Proveedores', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            {'codigo': '2.1.2', 'nombre': 'Sueldos y prestaciones por pagar', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            {'codigo': '2.1.3', 'nombre': 'Impuestos por pagar', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            {'codigo': '2.1.4', 'nombre': 'IVA Debito fiscal', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            {'codigo': '2.1.5', 'nombre': 'Préstamos a corto plazo', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            
            # Pasivo No Corriente
            {'codigo': '2.2', 'nombre': 'PASIVO NO CORRIENTE', 'tipo': 'PASIVO', 'es_cuenta_detalle': False},
            {'codigo': '2.2.1', 'nombre': 'Préstamos bancarios a largo plazo', 'tipo': 'PASIVO', 'es_cuenta_detalle': True},
            
            # ===== CAPITAL =====
            {'codigo': '3', 'nombre': 'CAPITAL', 'tipo': 'CAPITAL', 'es_cuenta_detalle': False},
            
            # Capital Social
            {'codigo': '3.1', 'nombre': 'CAPITAL SOCIAL', 'tipo': 'CAPITAL', 'es_cuenta_detalle': False},
            {'codigo': '3.1.1', 'nombre': 'Capital Social', 'tipo': 'CAPITAL', 'es_cuenta_detalle': True},
            {'codigo': '3.2', 'nombre': 'Utilidad del ejercicio', 'tipo': 'CAPITAL', 'es_cuenta_detalle': True},
            
            # ===== INGRESOS =====
            {'codigo': '4', 'nombre': 'INGRESOS', 'tipo': 'INGRESO', 'es_cuenta_detalle': False},
            {'codigo': '4.1', 'nombre': 'Ingresos por Licencias', 'tipo': 'INGRESO', 'es_cuenta_detalle': True},
            {'codigo': '4.2', 'nombre': 'Otros Ingresos', 'tipo': 'INGRESO', 'es_cuenta_detalle': True},
            
            # ===== COSTOS Y GASTOS =====
            {'codigo': '5', 'nombre': 'COSTOS Y GASTOS', 'tipo': 'GASTO', 'es_cuenta_detalle': False},
            
            # Costos
            {'codigo': '5.1', 'nombre': 'COSTOS', 'tipo': 'COSTO', 'es_cuenta_detalle': False},
            {'codigo': '5.1.1', 'nombre': 'Costo de ventas de licencia digitales', 'tipo': 'COSTO', 'es_cuenta_detalle': True},
            {'codigo': '5.1.2', 'nombre': 'Costo de producción de software', 'tipo': 'COSTO', 'es_cuenta_detalle': True},
            {'codigo': '5.1.3', 'nombre': 'Costos indirectos de desarrollo', 'tipo': 'COSTO', 'es_cuenta_detalle': True},
            
            # Gastos Operativos
            {'codigo': '5.2', 'nombre': 'GASTOS OPERATIVOS', 'tipo': 'GASTO', 'es_cuenta_detalle': False},
            
            # Gastos Administrativos
            {'codigo': '5.2.1', 'nombre': 'GASTOS ADMINISTRATIVOS', 'tipo': 'GASTO', 'es_cuenta_detalle': False},
            {'codigo': '5.2.1.1', 'nombre': 'Sueldos administrativos', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            {'codigo': '5.2.1.2', 'nombre': 'Servicios públicos y alquiler de oficinas', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            {'codigo': '5.2.1.3', 'nombre': 'Papelería y suministros', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            {'codigo': '5.1.2.4', 'nombre': 'Amortización de intangibles', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            
            # Gastos de Ventas
            {'codigo': '5.2.2', 'nombre': 'GASTOS DE VENTAS', 'tipo': 'GASTO', 'es_cuenta_detalle': False},
            {'codigo': '5.2.2.1', 'nombre': 'Publicidad y marketing digital', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            
            # Gastos Financieros
            {'codigo': '5.2.3', 'nombre': 'GASTOS FINANCIEROS', 'tipo': 'GASTO', 'es_cuenta_detalle': False},
            {'codigo': '5.2.3.1', 'nombre': 'Intereses pagados', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
            {'codigo': '5.2.3.2', 'nombre': 'Gastos bancarios', 'tipo': 'GASTO', 'es_cuenta_detalle': True},
        ]
        
        for cuenta_data in cuentas:
            # Buscar cuenta padre basado en el código
            codigo_padre = '.'.join(cuenta_data['codigo'].split('.')[:-1])
            cuenta_padre = None
            if codigo_padre:
                try:
                    cuenta_padre = Cuenta.objects.get(codigo=codigo_padre)
                except Cuenta.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Cuenta padre no encontrada: {codigo_padre}'))
            
            cuenta, created = Cuenta.objects.get_or_create(
                codigo=cuenta_data['codigo'],
                defaults={
                    'nombre': cuenta_data['nombre'],
                    'tipo': cuenta_data['tipo'],
                    'es_cuenta_detalle': cuenta_data['es_cuenta_detalle'],
                    'cuenta_padre': cuenta_padre
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Cuenta creada: {cuenta.codigo} - {cuenta.nombre}'))
            else:
                self.stdout.write(f'↻ Cuenta ya existe: {cuenta.codigo} - {cuenta.nombre}')
        
        self.stdout.write(self.style.SUCCESS('\n¡Catálogo de cuentas creado exitosamente!'))
        self.stdout.write(f'Total de cuentas en el sistema: {Cuenta.objects.count()}')