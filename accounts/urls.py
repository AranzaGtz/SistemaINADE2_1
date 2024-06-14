from django.urls import path
from accounts.vistas import views_usuarios, views_prospectos, views_empresas_contactos, views_autenticacion, views_home, views_cotizaciones, views_servicios

urlpatterns = [
    path('', views_autenticacion.dashboard, name='dashboard'),
    path('login/', views_autenticacion.login_view, name='login'),
    path('logout/', views_autenticacion.logout_view, name='logout'),
    path('mostrar_CustomUser/', views_autenticacion.mostrar_CustomUser,name='mostrar_CustomUser'),
        
    path('int_cotizaciones', views_cotizaciones.int_cotizaciones, name='int_cotizaciones'),
    
    path('home', views_home.home, name='home'),
    
    path('usuarios/',views_usuarios.usuario_list,name='usuario_list'),
    path('usuarios/new/',views_usuarios.usuario_create,name='usuario_create'),
    path('usuario/<username>/delete',views_usuarios.usuario_delete,name='usuario_delete'),
    path('usuario/<username>/edit', views_usuarios.usuario_update, name='usuario_edit'),
    path('usuario/<username>/edit2',views_usuarios.usuario_update2, name='usuario_edit2'),
    
    path('prospectos/',views_prospectos.prospecto_list, name='prospecto_list'),
    path('prospecto/new/',views_prospectos.prospecto_new, name='prospecto_new'),
    path('prospecto/create/',views_prospectos.prospecto_create, name='prospecto_create'),
    path('prospecto/<int:pk>/edit',views_prospectos.prospecto_edit,name='prospecto_edit'),
    path('prospecto/<int:pk>/update',views_prospectos.prospecto_update,name='prospecto_update'),
    path('prospecto/<int:pk>/delete',views_prospectos.prospecto_delete, name='prospecto_delete'),
    
    path('empresas-contactos/',views_empresas_contactos.empresa_cont_list, name='empresas_cont_list'),
    path('empresas/<int:pk>/edit/',views_empresas_contactos.empresa_edit, name='empresa_edit'),
    path('empresas/<int:pk>/update',views_empresas_contactos.empresa_update,name='empresa_update'),
    path('empresas/<int:pk>/delete/',views_empresas_contactos.empresa_delete, name='empresa_delete'),
    path('contacto/<int:pk>/edit/',views_empresas_contactos.contacto_edit,name='contacto_edit'),
    path('contacto/<int:pk>/update',views_empresas_contactos.contacto_update,name='contacto_update'),
    path('contacto/<int:pk>/delete/',views_empresas_contactos.contacto_delete, name='contacto_delete'),
    
    path('metodo/',views_servicios.metodos_list,name='metodos_list'),
    path('metodo/new/',views_servicios.metodo_create,name='metodo_create'),
    path('metodo/<int:pk>/delete',views_servicios.metodo_delete,name='metodo_delete'),
    
    path('servicios/',views_servicios.servicios_list,name='servicios_list'),
    path('servicio/new/',views_servicios.servicio_new,name='servicio_new'),
    path('servicio/create/', views_servicios.servicio_create, name='servicio_create'),
    path('servicio/<int:pk>/edit',views_servicios.servicio_edit,name='servicio_edit'),
    path('servicio/<int:pk>/update/', views_servicios.servicio_update, name='servicio_update'),
    path('servicio/<int:pk>/delete/',views_servicios.servicio_delete,name='servicio_delete'),

    
    
    # Define otras rutas según las vistas que hayas definido
]

