from django import forms
from catalog.models import Category, Product
from orders.models import Order


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "description", "price", "stock", "image_url", "is_active"]


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
