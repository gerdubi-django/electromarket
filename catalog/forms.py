from django import forms
from .models import Category, Product


class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "description", "price", "stock", "image_url", "is_active"]
