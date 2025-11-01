from django.core.management.base import BaseCommand
from contabilidad.models import Cuenta

class Command(BaseCommand):
    help = 'Carga las cuentas básicas incluyendo cuentas de IVA'
    
    def handle(self, *args, **options):
        cuentas_data = [
            # Activos
            {'codigo': '1', 'nombre': 'ACTIVO', 'tipo': 'activo', 'es_cuenta_detalle': False},
            {'codigo': '11', 'nombre': 'ACTIVO CORRIENTE', 'tipo': 'activo', 'es_cuenta_detalle': False},
            {'codigo': '1101', 'nombre': 'Caja General', 'tipo': 'activo', 'descripcion': 'Efectivo disponible en caja', 'acepta_iva': True},
            {'codigo': '1102', 'nombre': 'Bancos Nacionales', 'tipo': 'activo', 'descripcion': 'Depósitos en cuentas corrientes', 'acepta_iva': True},
            {'codigo': '1106', 'nombre': 'IVA Por Cobrar', 'tipo': 'activo', 'descripcion': 'Impuesto al Valor Agregado por cobrar'},
            
            # Pasivos
            {'codigo': '2', 'nombre': 'PASIVO', 'tipo': 'pasivo', 'es_cuenta_detalle': False},
            {'codigo': '21', 'nombre': 'PASIVO CORRIENTE', 'tipo': 'pasivo', 'es_cuenta_detalle': False},
            {'codigo': '2101', 'nombre': 'Proveedores', 'tipo': 'pasivo', 'descripcion': 'Deudas con proveedores locales', 'acepta_iva': True},
            {'codigo': '2105', 'nombre': 'IVA Por Pagar', 'tipo': 'pasivo', 'descripcion': 'Impuesto al Valor Agregado por pagar'},
            
            # Capital
            {'codigo': '3', 'nombre': 'CAPITAL', 'tipo': 'capital', 'es_cuenta_detalle': False},
            {'codigo': '3101', 'nombre': 'Capital Social', 'tipo': 'capital', 'descripcion': 'Aportaciones de los socios'},
            
            # Ingresos
            {'codigo': '4', 'nombre': 'INGRESOS', 'tipo': 'ingreso', 'es_cuenta_detalle': False},
            {'codigo': '4101', 'nombre': 'Ventas', 'tipo': 'ingreso', 'descripcion': 'Ventas de productos y servicios', 'acepta_iva': True},
            {'codigo': '4102', 'nombre': 'Ingresos por Servicios', 'tipo': 'ingreso', 'descripcion': 'Ingresos por prestación de servicios', 'acepta_iva': True},
            
            # Gastos
            {'codigo': '5', 'nombre': 'GASTOS', 'tipo': 'gasto', 'es_cuenta_detalle': False},
            {'codigo': '5101', 'nombre': 'Gastos de Oficina', 'tipo': 'gasto', 'descripcion': 'Consumo de papelería y suministros', 'acepta_iva': True},
            {'codigo': '5102', 'nombre': 'Gastos de Venta', 'tipo': 'gasto', 'descripcion': 'Gastos relacionados con ventas', 'acepta_iva': True},
            {'codigo': '5103', 'nombre': 'Compras', 'tipo': 'gasto', 'descripcion': 'Compras de mercadería', 'acepta_iva': True},
        ]
        
        for cuenta_data in cuentas_data:
            cuenta, created = Cuenta.objects.get_or_create(
                codigo=cuenta_data['codigo'],
                defaults=cuenta_data
            )
            if created:
                self.stdout.write(f'Cuenta creada: {cuenta.codigo} - {cuenta.nombre}')
        
        self.stdout.write(self.style.SUCCESS('Cuentas con IVA cargadas exitosamente!'))