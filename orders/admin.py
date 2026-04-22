from django.contrib import admin
from .models import Order, OrderItem, PaymentMethod


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "adjustment_percent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "subtotal", "adjustment_amount", "total", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username")
    inlines = [OrderItemInline]
