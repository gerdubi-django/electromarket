from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("django-admin/", admin.site.urls),
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("products/", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("admin/", include("dashboard.urls")),
)
