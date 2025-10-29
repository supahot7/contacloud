from django.db import models

# Create your models here.
class Cuenta(models.Model):
    codigo=models.CharField(max_length=20, unique=True)
    nombre=models.CharField(max_length=100)
    tipo=models.CharField(max_length=50)
    descripcion=models.TextField(blank=True)
    cuenta_padre=models.ForeignKey('self',  on_delete=models.SET_NULL, null=True, blank=True, related_name='hijas')

    es_cuenta_detalle=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Asiento(models.Model):
    fecha=models.DateField()
    descripcion=models.CharField()

class Partida(models.Model):
    asiento=models.ForeignKey(Asiento, related_name='partidas', on_delete=models.CASCADE)
    cuenta=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    debe=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    haber=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def clean(self):
        if self.debe > 0 and self.haber >0:
            raise ValidationError("Una partida no puede tener valores en debe y haber al mismo tiempo.")