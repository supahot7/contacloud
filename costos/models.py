from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class ManoObra(models.Model):
    """Modelo para registrar la mano de obra directa"""
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    TIPO_CONTRATO_CHOICES = [
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('temporal', 'Temporal'),
    ]
    
    nombre_trabajador = models.CharField(max_length=200, verbose_name="Nombre del Trabajador")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    costo_mensual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Costo Mensual"
    )
    fecha_registro = models.DateField(verbose_name="Fecha de Registro")

    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
 
    tipo_contrato = models.CharField(
        max_length=15,
        choices=TIPO_CONTRATO_CHOICES,
        default='tiempo_completo',
        verbose_name="Tipo de Contrato"
    )
   
    usuario = models.CharField(max_length=100, verbose_name="Usuario", blank=True)

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    
    class Meta:
        verbose_name = "Mano de Obra"
        verbose_name_plural = "Mano de Obra"
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.nombre_trabajador} - {self.cargo}"

#-------Modals para costos indirectos de fabricacion-----------
class CostoIndirecto(models.Model):  
    CATEGORIA_CHOICES = [
        ('servicios', 'Servicios'),
        ('mantenimiento', 'Mantenimiento'),
        ('depreciacion', 'Depreciación'),  
        ('seguro', 'Seguros'),
        ('otros', 'Otros')  
    ]

    concepto = models.CharField(max_length=200, verbose_name="Concepto")
    categoria = models.CharField(  
        max_length=15,
        choices=CATEGORIA_CHOICES,
        default='servicios',
        verbose_name="Categoría"
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Monto"
    )
    fecha_registro = models.DateField(verbose_name="Fecha de Registro")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")  # Cambié nombre
    
    # Agregar usuario 
    usuario = models.CharField(max_length=100, verbose_name="Usuario", blank=True)

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        verbose_name = "Costo Indirecto de Fabricación"
        verbose_name_plural = "Costos Indirectos de Fabricación"
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.concepto} - ${self.monto}"
    
#-------Modals planilla-----------------------#


class Planilla(models.Model):
    NOMBRE_CHOICE = [
        ('juan_perez', 'Juan Pérez'),
        ('maria_garcia', 'María García'),
        ('carlos_lopez', 'Carlos López'),
        ('ana_martinez', 'Ana Martínez'),
    ]

    PUESTO_CHOICE = [
        ('contador', 'Contador'),
        ('operario', 'Operario'),
        ('supervisor', 'Supervisor'),
        ('gerente', 'Gerente'),
        ('asistente', 'Asistente'),
    ]
    
    ANTIGUEDAD_CHOICE = [
        ('1-3', '1-3 años'),
        ('3-10', '3-10 años'),
        ('10+', '+10 años'),
    ]

    nombre = models.CharField(
        max_length=15,
        choices=NOMBRE_CHOICE,
        default='juan_perez',
        verbose_name="Nombre"
    )

    puesto = models.CharField(
        max_length=15,
        choices=PUESTO_CHOICE,
        default='contador',
        verbose_name="Puesto"
    )

    antiguedad = models.CharField(
        max_length=5,
        choices=ANTIGUEDAD_CHOICE,
        default='1-3',
        verbose_name="Antigüedad"
    )

    salario_nominal_mensual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Salario Nominal Mensual"
    )

    dias_trabajados = models.PositiveIntegerField(
        verbose_name="Días Trabajados",
        default=30
    )

    # Cálculos de beneficios
    sueldo_nominal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Sueldo Nominal",
        default=0
    )

    costo_semana_salarial = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Costo Semana Salarial",
        default=0
    )

    septimo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Séptimo",
        default=0
    )

    vacaciones = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Vacaciones",
        default=0
    )

    aguinaldo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Aguinaldo",
        default=0
    )

    calculo_salario_cancelado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Cálculo Salarial Cancelado",
        default=0
    )

    # ✅ CAMPOS FALTANTES AGREGADOS
    isss = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="ISSS",
        default=0
    )

    afp = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="AFP",
        default=0
    )

    incaf = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="INCAF",
        default=0
    )

    salario_total_semanal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="SALARIO TOTAL SEMANAL",
        default=0
    )

    salario_total_mensual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="SALARIO TOTAL MENSUAL",
        default=0
    )

    usuario = models.CharField(max_length=100, verbose_name="Usuario", blank=True)
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        verbose_name = "Planilla"
        verbose_name_plural = "Planillas"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.get_nombre_display()} - {self.get_puesto_display()}"

    
    def calcular_totales(self):
        """Método para calcular todos los valores de la planilla SEGÚN ANTIGÜEDAD"""
        from decimal import Decimal
        
        # CONSTANTES
        TASA_AFP = Decimal('0.0875')      # 8.75%
        TASA_ISSS = Decimal('0.0775')     # 7.75%
        TASA_INCAF = Decimal('0.01')      # 1%

        # 1. CÁLCULOS BÁSICOS
        dias = Decimal(str(max(1, self.dias_trabajados)))
        salario_diario = self.salario_nominal_mensual / dias

        print(f"DEBUG: salario_nominal_mensual={self.salario_nominal_mensual}, dias_trabajados={self.dias_trabajados}, salario_diario={salario_diario}")
        
        # Sueldo Nominal = Salario nominal mensual
        self.sueldo_nominal = salario_diario
        
        # Costo semana salarial = Salario diario * 5 días
        self.costo_semana_salarial = salario_diario * Decimal('5')
        
        # Séptimo = Salario diario * 2 días
        self.septimo = salario_diario * Decimal('2')
        
        # 2. VACACIONES - SIEMPRE 15 DÍAS
        dias_vacaciones = Decimal('15')
        self.vacaciones = (dias_vacaciones / Decimal('12')) * salario_diario
        
        # 3. AGUINALDO - VARÍA SEGÚN ANTIGÜEDAD
        if self.antiguedad == '1-3':
            dias_aguinaldo = Decimal('15')
        elif self.antiguedad == '3-10':
            dias_aguinaldo = Decimal('19')
        else:  # '10+'
            dias_aguinaldo = Decimal('21')
        
        self.aguinaldo = (dias_aguinaldo / Decimal('12')) * salario_diario
        
        # 4. Cálculo Salarial Cancelado
        self.calculo_salario_cancelado = ( self.costo_semana_salarial + self.septimo + self.vacaciones + self.aguinaldo)

        # 5. DEDUCCIONES
        self.isss = self.calculo_salario_cancelado * TASA_ISSS
        self.afp = self.calculo_salario_cancelado * TASA_AFP
        self.incaf = self.calculo_salario_cancelado * TASA_INCAF

        # 6. TOTALES
        self.salario_total_semanal = (self.calculo_salario_cancelado + self.isss + self.afp + self.incaf)
        
        self.salario_total_mensual = self.salario_total_semanal * Decimal('4')

    # ✅ MÉTODO SAVE DENTRO DE LA CLASE
    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular automáticamente los totales"""
        self.calcular_totales()
        super().save(*args, **kwargs)