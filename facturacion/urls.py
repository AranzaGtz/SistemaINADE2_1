# facturacion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_factura/<id_personalizado>', views.crear_factura, name='crear_factura'),
    path('cargar-csd/', views.cargar_csd, name='cargar_csd'),
    path('eliminar_csd/', views.eliminar_csd, name='eliminar_csd'),
    path('success/', views.success, name='success'),  # Define esta vista de éxito
    path('cf/', views.CF, name='cf'),
    path('obtener-datos-cotizacion/<int:cotizacion_id>/', views.obtener_datos_cotizacion, name='obtener_datos_cotizacion'),
    path('facturas/',views.facturas_list, name = 'facturas_list'),
    path('factura/detalle/<cfdi_id>/', views.factura_detalle, name='factura_detalle'),
    path('factura/cancelar_cfdi/', views.cancelar_factura,name='cancelar_factura'),
    path('factura/comprobante_cfdi/<cfdi_id>',views.comprobante_factura,name='comprobante_factura'),
    path('download/comprobante/<str:id_factura>/<str:file_type>/', views.download_comprobante, name='download_comprobante'),
    path('download/factura/<str:id_factura>/<str:file_type>/', views.download_factura, name='download_factura'),
    path('email/', views.send_email_view, name='send_email_view'),
]
