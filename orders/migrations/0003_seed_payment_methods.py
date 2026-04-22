from decimal import Decimal
from django.db import migrations


def seed_payment_methods(apps, schema_editor):
    payment_method_model = apps.get_model("orders", "PaymentMethod")
    default_methods = [
        ("Efectivo", "cash", Decimal("-5.00")),
        ("Transferencia", "bank-transfer", Decimal("-3.00")),
        ("Débito", "debit-card", Decimal("0.00")),
        ("Crédito", "credit-card", Decimal("8.00")),
        ("Cuotas", "installments", Decimal("12.00")),
        ("Mercado Pago", "mercado-pago", Decimal("4.00")),
    ]
    for name, code, adjustment_percent in default_methods:
        payment_method_model.objects.update_or_create(
            code=code,
            defaults={"name": name, "adjustment_percent": adjustment_percent, "is_active": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_paymentmethod_order_adjustment_amount_order_subtotal_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_payment_methods, migrations.RunPython.noop),
    ]
