from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from .models import Order
from .services import create_order_from_cart


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            order = create_order_from_cart(request.user)
            messages.success(request, f"Order #{order.id} created")
            return redirect("orders:history")
        except Exception as error:
            messages.error(request, str(error))
            return redirect("cart:detail")


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


class SimulatePaymentView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == Order.STATUS_PENDING:
            order.status = Order.STATUS_PAID
            order.save(update_fields=["status"])
            messages.success(request, "Payment simulated successfully")
        return redirect("orders:history")
