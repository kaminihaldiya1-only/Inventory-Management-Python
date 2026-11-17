
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'product_name',
        'product_code',
        'category',
        'quantity',
        'price',
        'supplier',
    )

    search_fields = (
        'product_name',
        'product_code',
        'category',
    )

    list_filter = ('category',)
