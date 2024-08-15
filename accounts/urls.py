from django.urls import path
from accounts import views
from accounts.views import notificaciones, marcar_notificacion_leida, borrar_notificacion
from accounts.vistas import views_clientes, views_cotizaciones_aceptadas, views_empresas, views_guia, views_orden_trabajo, views_usuarios, views_prospectos, views_autenticacion, views_home, views_cotizaciones, views_servicios, views_correos, views_organizacion
from django.contrib.auth import views as auth_views
from accounts.vistas.views_autenticacion import CustomPasswordResetView


urlpatterns = [

    #   ---     LOGIN       ---

    path('', views_autenticacion.dashboard, name='dashboard'),
    path('login/', views_autenticacion.login_view, name='login'),
    path('logout/', views_autenticacion.logout_view, name='logout'),

    #   ---     RECUPERACIÓN DE CONTRASEÑA       ---

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/autenticacion/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/autenticacion/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/autenticacion/password_reset_complete.html'), name='password_reset_complete'),

    #   ---     INTERFAZ NOTIFICACIONES       ---
    
    path('notificaciones/', notificaciones, name='notificaciones'),
    path('notificacion/leida/<int:pk>/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificacion/borrar/<int:pk>/', views.borrar_notificacion, name='borrar_notificacion'),
    
    #   ---     INTERFAZ HOME       ---

    path('home/', views_home.home, name='home'),

    #   ---     INTERFAZ USUARIOS       ---

    path('usuarios/', views_usuarios.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views_usuarios.usuario_create, name='usuario_create'),
    path('usuarios/eliminar/<id>/',views_usuarios.usuario_delete, name='usuario_delete'),
    path('usuarios/editar/<username>/',views_usuarios.usuario_update, name='usuario_edit'),

    #   ---     INTERFAZ CLIENTES       ---
    path('agregar-titulo/', views_clientes.agregar_titulo, name='agregar_titulo'),
    path('cerrar-ventana/', views_clientes.cerrar_ventana, name='cerrar_ventana'),
    path('obtener-titulos/', views_clientes.obtener_titulos, name='obtener_titulos'),
    path('clientes/', views_clientes.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views_clientes.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views_clientes.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', views_clientes.cliente_delete, name='cliente_delete'),

    #   ---     INTERFAZ PROSPECTOS       ---

    path('prospectos/', views_prospectos.prospecto_list, name='prospecto_list'),
    path('prospectos/nuevo/', views_prospectos.prospecto_create, name='prospecto_create'),
    path('prospectos/eliminar/<int:pk>/',  views_prospectos.prospecto_delete, name='prospecto_delete'),
    path('prospectos/cotizacion/nueva/<persona_id>/', views_prospectos.cotizacion_form_con_cliente, name='cotizacion_form_con_cliente'),

    #   ---     INTERFAZ EMPRESAS       ---

    path('empresas-contactos/', views_empresas.empresa_cont_list, name='empresas_cont_list'),
    path('empresa/nueva/', views_empresas.empresa_create, name='empresa_create'),
    path('empresas/editar/<int:pk>/', views_empresas.empresa_edit, name='empresa_edit'),
    path('empresas/actualizar<int:pk>/', views_empresas.empresa_update, name='empresa_update'),
    path('empresas/eliminar/<int:pk>/', views_empresas.empresa_delete, name='empresa_delete'),


    #   ---     INTERFAZ METODOS       ---

    path('metodo/new/', views_servicios.metodo_create, name='metodo_create'),
    path('metodo/delete/<int:pk>/', views_servicios.metodo_delete, name='metodo_delete'),

    #   ---     INTERFAZ SERVICIOS       ---

    path('servicios/', views_servicios.servicios_list, name='servicios_list'),
    path('servicios/nuevo/', views_servicios.servicio_create, name='servicio_create'),
    path('servicios/edit/<int:pk>/', views_servicios.servicio_edit, name='servicio_edit'),
    path('servicios/delete/<int:pk>/', views_servicios.servicio_delete, name='servicio_delete'),

    #   ---     INTERFAZ COTIZACIONES       ---
    
    path('agregar-servicio/', views_cotizaciones.agregar_servicio, name='agregar_servicio'),
    path('cotizaciones/', views_cotizaciones.cotizaciones_list, name='cotizaciones_list'),
    path('obtener_datos_cliente/<int:cliente_id>/', views_cotizaciones.obtener_datos_cliente, name='obtener_datos_cliente'),
    path('obtener_datos_servicio/<int:servicio_id>/', views_cotizaciones.obtener_datos_servicio, name='obtener_datos_servicio'),
    path('cotizaciones/nueva/<int:persona_id>', views_cotizaciones.cotizacion_form, name='cotizacion_form'),
    path('persona/<int:persona_id>/cotizacion/<int:cotizacion_id>/', views_cotizaciones.cotizacion_form, name='edit_cotizacion'),
    path('cotizaciones/<pk>/detalle', views_cotizaciones.cotizacion_detalle, name='cotizacion_detalle'),
    path('cotizaciones/<int:pk>/delete/', views_cotizaciones.cotizacion_delete, name='cotizacion_delete'),
    path('cotizaciones/editar/<int:pk>/', views_cotizaciones.cotizacion_edit, name='cotizaciones_editar'),
    path('cotizaciones/<int:pk>/duplicar/', views_cotizaciones.cotizacion_duplicar, name='cotizacion_duplicar'),
    path('cotizacion/<int:pk>/pdf/', views_cotizaciones.cotizacion_pdf, name='cotizacion_pdf'),
    path('cotizacion/pdf', views_cotizaciones.generar_pdf_cotizacion, name='generar_pdf_cotizacion'),
    path('cotizacion/<int:pk>/actualizar_estado/', views_cotizaciones.actualizar_estado, name='actualizar_estado'),
    
    #   ---     INTERFAZ COTIZACIONES ACEPTADAS      ---
        
    path('agregar-receptor/', views_cotizaciones_aceptadas.agregar_receptor, name='agregar_receptor'),
    path('cotizaciones_aceptadas/', views_cotizaciones_aceptadas.cotizaciones_aceptadas_list,name='cotizaciones_aceptadas_list'),
    path('cotizaciones_aceptadas/generar_orden_trabajo/<pk>', views_cotizaciones_aceptadas.generar_orden_trabajo , name='generar_orden_trabajo'),

    
    #   ---     INTERFAZ ORDENES DE TRABAJO     ---
    
    path('ordenes_de_trabajo/', views_orden_trabajo.ordenes_list, name='ordenes_list'),
    path('orden_trabajo/<id_personalizado>/', views_orden_trabajo.detalle_orden_trabajo, name='detalle_orden_trabajo'),
    path('orden_trabajo/<id_personalizado>/pdf', views_orden_trabajo.orden_trabajo_pdf, name= 'orden_trabajo_pdf'),

    

    #   ---     ENVIOS DE CORREOS       ---

    path('cotizacion/<int:pk>/seleccionar_correos/', views_correos.seleccionar_correos, name='seleccionar_correos'),
    path('cotizacion/<int:pk>/confirmar_recepcion/', views_correos.confirmar_recepcion, name='confirmar_recepcion'),
    path('cotizacion/terminada', views_correos.confirmacion_recepcion, name='confirmacion_recepcion'),
    path('formulario_descarga_subida/<int:pk>/<usuario>/', views_correos.formulario_descarga_subida, name='formulario_descarga_subida'),
    path('orden_trabajo/envio/<pk>/<receptor>/', views_correos.enviar_orden, name = 'enviar_orden'),
    
    #   ---     ORGANIZACION       ---

    path('organizacion/terminos/', views_organizacion.editar_organizacion, name='editar_organizacion'),
    path('formatos/', views_organizacion.formatos, name='formatos'),
    path('queja/', views_organizacion.enviar_queja, name='enviar_queja'),

    
    #   ---     GUIA DE OPERACIONES       ---
    path('guia_operaciones/', views_guia.guia_operaciones, name='guia_operaciones'),
    path('guia_operaciones/usuarios', views_guia.guia_add_u, name='guia_add_u'),

    # Define otras rutas según las vistas que hayas definido
]
