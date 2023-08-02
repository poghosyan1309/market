from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app_account.urls', namespace='account')),
    path('products/', include('app_product.urls', namespace='product')),
    path('stores/', include('app_store.urls', namespace='store')),
    path('tickets/', include('app_ticket.urls', namespace='ticket')),

]
