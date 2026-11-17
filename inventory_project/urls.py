from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login and Logout
    path('accounts/', include('django.contrib.auth.urls')),

    # Inventory Dashboard
    path('', include('inventory.urls')),
]