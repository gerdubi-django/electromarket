from decimal import Decimal
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem


def create_order_from_cart(user) -> Order:
    cart = Cart.objects.select_for_update().prefetch_related("items__product").get(user=user)
    if not cart.items.exists():
        raise ValueError("Cart is empty")

    with transaction.atomic():
        order = Order.objects.create(user=user)
        total = Decimal("0.00")

        for item in cart.items.all():
            product = item.product
            if item.quantity > product.stock:
                raise ValueError(f"Not enough stock for {product.name}")

            product.stock -= item.quantity
            product.save(update_fields=["stock"])
            line_total = product.price * item.quantity
            total += line_total
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
            )

        order.total = total
        order.save(update_fields=["total"])
        cart.items.all().delete()
        return order
