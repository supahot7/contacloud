from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    ROL_CONTADOR=1
    ROL_AUDITOR=2

    ROLES_CHOICES=(
        (ROL_CONTADOR, 'Contador'),
        (ROL_AUDITOR, 'Auditor'),
    )

    rol=models.PositiveSmallIntegerField(
        choices=ROLES_CHOICES,
        default=ROL_CONTADOR
    )

    USERNAME_FIELD='username'
    
    def __str__(self):
        return self.username