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
    acepta_iva = models.BooleanField(default=False)  # Nueva campo para cuentas que aceptan IVA

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def get_absolute_url(self):
        return reverse('contabilidad:detalle_cuenta', kwargs={'pk': self.pk})
    
    def get_saldo(self):
        """Calcula el saldo de la cuenta"""
        total_debe = self.partidas.aggregate(Sum('debe'))['debe__sum'] or 0
        total_haber = self.partidas.aggregate(Sum('haber'))['haber__sum'] or 0
        
        if self.tipo in ['activo', 'gasto']:
            return total_debe - total_haber
        else:
            return total_haber - total_debe

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