from django.urls import path
from accounts.vistas import views_clientes, views_usuarios, views_prospectos, views_empresas_contactos, views_autenticacion, views_home, views_cotizaciones, views_servicios, views_correos
from django.contrib.auth import views as auth_views
from accounts.vistas.views_autenticacion import CustomPasswordResetView


urlpatterns = [
    
    #   ---     LOGIN       ---
    
    path('', views_autenticacion.dashboard, name='dashboard'),
    path('login/', views_autenticacion.login_view, name='login'),
    path('logout/', views_autenticacion.logout_view, name='logout'),
    path('mostrar_CustomUser/', views_autenticacion.mostrar_CustomUser,name='mostrar_CustomUser'),
    
    #   ---     RECUPERACIÓN DE CONTRASEÑA       ---
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/autenticacion/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/autenticacion/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/autenticacion/password_reset_complete.html'), name='password_reset_complete'),
    
    #   ---     INTERFAZ HOME       ---
    
    path('home/', views_home.home, name='home'),
    
    #   ---     INTERFAZ USUARIOS       ---
    
    path('usuarios/',views_usuarios.usuario_list,name='usuario_list'),
    path('usuarios/nuevo/',views_usuarios.usuario_create,name='usuario_create'),
    path('usuarios/eliminar/<username>/',views_usuarios.usuario_delete,name='usuario_delete'),
    path('usuarios/editar/<username>/', views_usuarios.usuario_update, name='usuario_edit'),
    path('usuarios/editar/<username>/',views_usuarios.usuario_update2, name='usuario_edit2'),
    
    #   ---     INTERFAZ CLIENTES       ---

    path('clientes/', views_clientes.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views_clientes.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views_clientes.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', views_clientes.cliente_delete, name='cliente_delete'),

    
    #   ---     INTERFAZ PROSPECTOS       ---
    
    path('prospectos/',views_prospectos.prospecto_list, name='prospecto_list'),
    path('prospectos/nuevo/',views_prospectos.prospecto_create, name='prospecto_create'),
    path('prospectos/eliminar/<int:pk>/',views_prospectos.prospecto_delete, name='prospecto_delete'),
    path('prospectos/cotizacion/nueva/<persona_id>/<str:moneda>/',views_prospectos.cotizacion_form_con_cliente,name='cotizacion_form_con_cliente'),
    
    #   ---     INTERFAZ EMPRESAS       ---
    
    path('empresas-contactos/',views_empresas_contactos.empresa_cont_list, name='empresas_cont_list'),
    path('empresa/nueva/', views_empresas_contactos.empresa_create, name='empresa_create'),
    path('empresas/editar/<int:pk>/',views_empresas_contactos.empresa_edit, name='empresa_edit'),
    path('empresas/actualizar<int:pk>/',views_empresas_contactos.empresa_update,name='empresa_update'),
    path('empresas/eliminar/<int:pk>/',views_empresas_contactos.empresa_delete, name='empresa_delete'),
    
    path('contacto/editar/<int:pk>/',views_empresas_contactos.contacto_edit,name='contacto_edit'),
    path('contacto/actualizar/<int:pk>/',views_empresas_contactos.contacto_update,name='contacto_update'),
    path('contacto/eliminar/<int:pk>/',views_empresas_contactos.contacto_delete, name='contacto_delete'),
    
    #   ---     INTERFAZ METODOS       ---
    
    path('metodo/new/',views_servicios.metodo_create,name='metodo_create'),
    path('metodo/<int:pk>/delete/',views_servicios.metodo_delete,name='metodo_delete'),
    
    #   ---     INTERFAZ SERVICIOS       ---
    
    path('servicios/',views_servicios.servicios_list,name='servicios_list'),
    path('servicios/nuevo/', views_servicios.servicio_create, name='servicio_create'),
    path('servicios/edit/<int:pk>/',views_servicios.servicio_edit,name='servicio_edit'),
    path('servicios/delete/<int:pk>/',views_servicios.servicio_delete,name='servicio_delete'),
    
    #   ---     INTERFAZ COTIZACIONES       ---
    
    path('cotizaciones/', views_cotizaciones.cotizaciones_list, name='cotizaciones_list'),
    path('obtener_datos_cliente/<int:cliente_id>/', views_cotizaciones.obtener_datos_cliente, name='obtener_datos_cliente'),
     path('obtener_datos_servicio/<int:servicio_id>/', views_cotizaciones.obtener_datos_servicio, name='obtener_datos_servicio'),
    path('cotizaciones/nueva/', views_cotizaciones.cotizacion_form, name='cotizacion_form'),
    path('cotizaciones/cliente/nueva', views_cotizaciones.cotizaciones_prospecto_create, name='cotizaciones_prospecto_create'),
    path('cotizaciones/editar/<int:pk>/', views_cotizaciones.cotizacion_edit, name='cotizacion_edit'),
    path('cotizaciones/<int:pk>/detalle', views_cotizaciones.cotizacion_detalle, name='cotizacion_detalle'),
    path('cotizaciones/<int:pk>/delete/', views_cotizaciones.cotizacion_delete,name='cotizacion_delete'),

    path('cotizacion/<int:pk>/pdf/',views_cotizaciones.cotizacion_pdf,name='cotizacion_pdf'),
    path('cotizaciones/<int:pk>/duplicar/',views_cotizaciones.cotizacion_duplicar,name='cotizacion_duplicar'),
    
    #   ---     INTERFAZ TERMINOS Y AVISOS       ---
    
    path('terminos/',views_cotizaciones.terminos_avisos, name='terminos_avisos'),
    
    #   ---     ENVIOS DE CORREOS       ---
    
    path('enviar_correo/', views_correos.enviar_correo, name='enviar_correo'),
    path('cotizacion/<int:pk>/seleccionar_correos/', views_correos.seleccionar_correos, name='seleccionar_correos'),
    path('cotizacion/<int:pk>/confirmar_recepcion/', views_correos.confirmar_recepcion, name='confirmar_recepcion'),
    path('cotizacion/terminada', views_correos.confirmacion_recepcion, name='confirmacion_recepcion'),

    # Define otras rutas según las vistas que hayas definido
]

