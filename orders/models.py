from django.db import models

# Create your models here.
# orders/models.py
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("shipped", "Shipped"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # سعر وقت الطلب
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
