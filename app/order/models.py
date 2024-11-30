from django.db import models
from shop.models import Product
import uuid

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('contrareembolso', 'Contra reembolso'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='tarjeta')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
