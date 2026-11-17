from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('add-product/', views.add_product, name='add_product'),

    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),

    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),

    path('product-details/<int:id>/', views.product_details, name='product_details'),
]