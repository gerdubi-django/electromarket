from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, View
from catalog.models import Product
from orders.models import PaymentMethod
from .models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _created_cart = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        context["payment_methods"] = PaymentMethod.objects.filter(is_active=True)
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        try:
            quantity = max(1, int(request.POST.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1

        cart, _created_cart = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        new_quantity = quantity if created else item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, _("No hay stock suficiente"))
            return redirect("catalog:product_detail", slug=product.slug)

        item.quantity = new_quantity
        item.save(update_fields=["quantity"])
        messages.success(request, _("Producto agregado al carrito"))
        return redirect("cart:detail")


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        try:
            quantity = max(1, int(request.POST.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1

        if quantity > item.product.stock:
            messages.error(request, _("No hay stock suficiente"))
        else:
            item.quantity = quantity
            item.save(update_fields=["quantity"])
            messages.success(request, _("Carrito actualizado"))
        return redirect("cart:detail")


class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.info(request, _("Producto eliminado del carrito"))
        return redirect("cart:detail")
