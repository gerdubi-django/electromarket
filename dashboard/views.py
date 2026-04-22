from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from catalog.models import Category, Product
from orders.models import Order
from .forms import CategoryForm, OrderStatusForm, ProductForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_sales"] = Order.objects.aggregate(total=Sum("total"))["total"] or 0
        context["order_count"] = Order.objects.count()
        context["recent_orders"] = Order.objects.select_related("user")[:8]
        return context


class ProductListView(AdminRequiredMixin, ListView):
    template_name = "dashboard/products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "dashboard/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("dashboard:products")


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "dashboard/product_form.html"
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy("dashboard:products")


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "dashboard/confirm_delete.html"
    model = Product
    success_url = reverse_lazy("dashboard:products")


class CategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = "dashboard/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard:products")


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "dashboard/confirm_delete.html"
    model = Category
    success_url = reverse_lazy("dashboard:products")


class OrderListView(AdminRequiredMixin, ListView):
    template_name = "dashboard/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("user", "payment_method").prefetch_related("items")


class OrderStatusUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "dashboard/order_status_form.html"
    form_class = OrderStatusForm
    model = Order
    success_url = reverse_lazy("dashboard:orders")
