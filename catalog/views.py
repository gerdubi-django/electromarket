from django.db.models import Q
from django.views.generic import DetailView, ListView
from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    paginate_by = 12
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        search = self.request.GET.get("search", "").strip()
        category = self.request.GET.get("category", "").strip()
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if category:
            queryset = queryset.filter(category__slug=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")
