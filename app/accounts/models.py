from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('contrareembolso', 'Contra reembolso'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dirección = models.CharField(max_length=255)
    código_postal = models.IntegerField(max_length=5)
    ciudad = models.CharField(max_length=50)
    método_pago = models.CharField(
        max_length=15,
        choices=PAYMENT_METHOD_CHOICES,
        default='tarjeta',
    )
    