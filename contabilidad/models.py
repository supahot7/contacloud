from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from usuarios.models import Usuario

class Cuenta(models.Model):
    TIPOS_CUENTA = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('capital', 'Capital'),
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_CUENTA)
    descripcion = models.TextField(blank=True)
    cuenta_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='hijas')
    es_cuenta_detalle = models.BooleanField(default=True)
    acepta_iva = models.BooleanField(default=False)
    grupo = models.CharField(max_length=20, blank=True)  # NUEVO CAMPO

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Asiento(models.Model):
    ESTADOS_ASIENTO = [
        ('borrador', 'Borrador'),
        ('contabilizado', 'Contabilizado'),
        ('anulado', 'Anulado'),
    ]
    
    fecha = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=200)
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_ASIENTO, default='contabilizado')
    tiene_iva = models.BooleanField(default=False)  # Nuevo campo para identificar asientos con IVA
    monto_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Monto total del asiento

    class Meta:
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f"Asiento {self.id} - {self.fecha}"
    
    def clean(self):
        """Valida que el asiento esté balanceado"""
        partidas = self.partidas.all()
        total_debe = sum(partida.debe for partida in partidas)
        total_haber = sum(partida.haber for partida in partidas)
        
        if total_debe != total_haber:
            raise ValidationError("El asiento no está balanceado. Débito total debe ser igual al crédito total.")
    
    def save(self, *args, **kwargs):
        # Calcular monto total antes de guardar
        if self.pk:
            partidas = self.partidas.all()
            self.monto_total = sum(partida.debe for partida in partidas) + sum(partida.haber for partida in partidas)
        super().save(*args, **kwargs)

class Partida(models.Model):
    asiento = models.ForeignKey(Asiento, related_name='partidas', on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, related_name='partidas', on_delete=models.PROTECT)
    debe = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    haber = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    descripcion = models.CharField(max_length=200, blank=True)
    es_iva = models.BooleanField(default=False)  # Nuevo campo para identificar partidas de IVA
    monto_base = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Monto sin IVA
    monto_iva = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Monto de IVA
    
    class Meta:
        ordering = ['-asiento__fecha', 'id']

    def clean(self):
        if self.debe > 0 and self.haber > 0:
            raise ValidationError("Una partida no puede tener valores en debe y haber al mismo tiempo.")
        if self.debe < 0 or self.haber < 0:
            raise ValidationError("Los valores de débito y crédito no pueden ser negativos.")
    
    def __str__(self):
        return f"{self.cuenta.codigo} - D: {self.debe} H: {self.haber}"
    
    @property
    def monto_total(self):
        """Retorna el monto total (base + IVA)"""
        return self.monto_base + self.monto_iva
    
# models.py - Actualizar el modelo Licencia
class Licencia(models.Model):
    ESTADOS_LICENCIA = [
        ('disponible', 'Disponible'),
        ('vendida', 'Vendida'),
        ('inactiva', 'Inactiva'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_adquisicion = models.DateField(default=timezone.now)
    costo_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cantidad_disponible = models.IntegerField(default=0)
    cantidad_total = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_LICENCIA, default='disponible')
    valor_total_inventario_db = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Valor Total Inventario"
    )
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular automáticamente el valor total"""
        # Calcular el valor total antes de guardar
        self.valor_total_inventario_db = self.cantidad_disponible * self.costo_unitario
        super().save(*args, **kwargs)
    
    def vender_licencia(self, cantidad=1):
        """Método para vender licencias y actualizar el inventario"""
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        if self.cantidad_disponible < cantidad:
            raise ValidationError(f"No hay suficientes licencias disponibles. Disponibles: {self.cantidad_disponible}")
        
        self.cantidad_disponible -= cantidad
        # El valor_total_inventario_db se actualizará automáticamente en save()
        self.save()
        
        # Si no hay más licencias disponibles, cambiar estado
        if self.cantidad_disponible == 0:
            self.estado = 'vendida'
            self.save()
    
    def agregar_licencias(self, cantidad):
        """Método para agregar más licencias al inventario"""
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        self.cantidad_disponible += cantidad
        self.cantidad_total += cantidad
        
        # Si había estado como vendida, cambiar a disponible
        if self.estado == 'vendida':
            self.estado = 'disponible'
        
        # El valor_total_inventario_db se actualizará automáticamente en save()
        self.save()
    
    @property
    def valor_total_inventario(self):
        """Propiedad para obtener el valor total (solo lectura)"""
        return self.valor_total_inventario_db