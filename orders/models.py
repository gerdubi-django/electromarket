from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Product


class PaymentMethod(models.Model):
    name = models.CharField(max_length=80, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    adjustment_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_SHIPPED = "shipped"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pendiente")),
        (STATUS_PAID, _("Pagado")),
        (STATUS_SHIPPED, _("Enviado")),
        (STATUS_COMPLETED, _("Completado")),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=180)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
