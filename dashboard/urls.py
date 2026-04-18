from django.urls import path
from .views import (
    DashboardHomeView,
    CategoryCreateView,
    CategoryDeleteView,
    OrderListView,
    OrderStatusUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductListView,
    ProductUpdateView,
)

app_name = "dashboard"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/new/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("categories/new/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order_status"),
]
