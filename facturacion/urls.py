# facturacion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_factura/<id_personalizado>', views.crear_factura, name='crear_factura'),
    path('cargar-csd/', views.cargar_csd, name='cargar_csd'),
    path('success/', views.success, name='success'),  # Define esta vista de éxito
    path('cf/', views.CF, name='cf'),
    path('obtener-datos-cotizacion/<int:cotizacion_id>/', views.obtener_datos_cotizacion, name='obtener_datos_cotizacion'),
    path('facturas/',views.facturas_list, name = 'facturas_list'),
    path('factura/detalle/<cfdi_id>/', views.factura_detalle, name='factura_detalle'),
    path('factura/comprobante_pago/<str:cfdi_id>/', views.generar_comprobante_pago, name='generar_comprobante_pago'),
    path('factura/<id_factura>', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('factura/xml/<str:id_factura>/', views.generar_factura_xml, name='generar_factura_xml'),
    path('factura/cancelar/', views.cancelar_factura,name='cancelar_factura'),
]
