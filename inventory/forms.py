
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'product_name',
            'product_code',
            'category',
            'description',
            'quantity',
            'price',
            'supplier'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_product_name(self):
        name = self.cleaned_data['product_name'].strip()

        if not name:
            raise forms.ValidationError(
                "Product name cannot be empty."
            )

        return name

    def clean_product_code(self):
        code = self.cleaned_data['product_code'].strip()

        if not code:
            raise forms.ValidationError(
                "Product code cannot be empty."
            )

        return code

    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price
