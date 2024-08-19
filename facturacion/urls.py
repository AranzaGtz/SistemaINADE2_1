# facturacion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_factura/<id_personalizado>', views.crear_factura, name='crear_factura'),
]
