# facturacion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_factura/<id_personalizado>', views.crear_factura, name='crear_factura'),
    path('cargar-csd/', views.cargar_csd, name='cargar_csd'),
    path('success/', views.success, name='success'),  # Define esta vista de éxito
    path('cf/', views.CF, name='cf'),
    path('obtener-datos-cotizacion/<int:cotizacion_id>/', views.obtener_datos_cotizacion, name='obtener_datos_cotizacion'),
    path('agregar-sucursal/',views.agregar_sucursal, name='agregar_sucursal'),
    path('agregar_almacen/',views.agregar_almacen, name='agregar_almacen'),
]
