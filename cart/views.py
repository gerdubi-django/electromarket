from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from catalog.models import Product
from .models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = max(1, int(request.POST.get("quantity", 1)))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, _ = CartItem.objects.get_or_create(cart=cart, product=product)

        if item.quantity + quantity > product.stock:
            messages.error(request, "Not enough stock")
            return redirect("catalog:product_detail", slug=product.slug)

        item.quantity += quantity
        item.save(update_fields=["quantity"])
        messages.success(request, "Product added to cart")
        return redirect("cart:detail")


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = max(1, int(request.POST.get("quantity", 1)))
        if quantity > item.product.stock:
            messages.error(request, "Not enough stock")
        else:
            item.quantity = quantity
            item.save(update_fields=["quantity"])
            messages.success(request, "Cart updated")
        return redirect("cart:detail")


class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.info(request, "Item removed")
        return redirect("cart:detail")
