from decimal import Decimal

from django.db import transaction

from cart.models import Cart

from .models import Order, OrderItem, PaymentMethod


def create_order_from_cart(user, payment_method_id=None) -> Order:
    with transaction.atomic():
        cart = (
            Cart.objects.select_for_update()
            .prefetch_related("items__product")
            .get(user=user)
        )
        if not cart.items.exists():
            raise ValueError("El carrito está vacío")

        payment_method = None
        if payment_method_id:
            payment_method = (
                PaymentMethod.objects.select_for_update()
                .filter(id=payment_method_id, is_active=True)
                .first()
            )
            if payment_method is None:
                raise ValueError("Medio de pago inválido")

        order = Order.objects.create(user=user, payment_method=payment_method)
        subtotal = Decimal("0.00")

        for item in cart.items.all():
            product = item.product
            product = type(product).objects.select_for_update().get(id=product.id)
            if item.quantity > product.stock:
                raise ValueError(f"Stock insuficiente para {product.name}")

            product.stock -= item.quantity
            product.save(update_fields=["stock"])
            line_total = product.price * item.quantity
            subtotal += line_total
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
            )

        adjustment_amount = Decimal("0.00")
        if payment_method:
            adjustment_amount = (subtotal * payment_method.adjustment_percent) / Decimal("100")

        order.subtotal = subtotal
        order.adjustment_amount = adjustment_amount
        order.total = subtotal + adjustment_amount
        order.save(update_fields=["subtotal", "adjustment_amount", "total"])
        cart.items.all().delete()
        return order
