
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm


# Dashboard
@login_required
def dashboard(request):

    total_products = Product.objects.count()

    total_quantity = Product.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    low_stock = Product.objects.filter(quantity__lt=10).count()

    inventory_value = Product.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('price') * F('quantity'),
                output_field=DecimalField(
                    max_digits=15,
                    decimal_places=2
                )
            )
        )
    )['total'] or 0

    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')
    sort_by = request.GET.get('sort', 'newest')

    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(product_code__icontains=search_query)
        )

    if selected_category:
        products = products.filter(category=selected_category)

    if stock_filter == 'low':
        products = products.filter(quantity__lt=10)

    sorting_options = {
        'newest': '-created_at',
        'name': 'product_name',
        'price_low': 'price',
        'price_high': '-price',
        'quantity_low': 'quantity',
        'quantity_high': '-quantity',
    }

    products = products.order_by(
        sorting_options.get(sort_by, '-created_at')
    )

    paginator = Paginator(products, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Product.objects.values_list(
        'category', flat=True
    ).distinct().order_by('category')

    context = {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'low_stock': low_stock,
        'inventory_value': inventory_value,
        'products': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': categories,
        'selected_category': selected_category,
        'stock_filter': stock_filter,
        'sort_by': sort_by,
    }

    return render(request, 'inventory/dashboard.html', context)


# Add Product
@login_required
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'inventory/add_product.html', {
        'form': form
    })


# Edit Product
@login_required
def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/edit_product.html', {
        'form': form,
        'product': product
    })


# Delete Product
@login_required
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('dashboard')

    return render(request, 'inventory/delete_product.html', {
        'product': product
    })


# Product Details
@login_required
def product_details(request, id):

    product = get_object_or_404(Product, id=id)

    return render(request, 'inventory/product_details.html', {
        'product': product
    })
