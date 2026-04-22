from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, View
from .models import Order
from .services import create_order_from_cart


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        payment_method_id = request.POST.get("payment_method")
        try:
            order = create_order_from_cart(request.user, payment_method_id=payment_method_id)
            messages.success(request, _("Pedido #%(id)s generado correctamente") % {"id": order.id})
            return redirect("orders:history")
        except Exception as error:
            messages.error(request, str(error))
            return redirect("cart:detail")


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("payment_method").prefetch_related("items")


class SimulatePaymentView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == Order.STATUS_PENDING:
            order.status = Order.STATUS_PAID
            order.save(update_fields=["status"])
            messages.success(request, _("Pago simulado correctamente"))
        return redirect("orders:history")
