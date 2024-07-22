from django.shortcuts import render
from accounts.models import OrdenTrabajo
from django.core.paginator import Paginator

#    VISTA PARA ORDENES DE TRABAJO
def ordenes_list(request):
     # Notificación
     notificaciones = request.user.notificacion_set.all()
     notificaciones_no_leidas = notificaciones.filter(leido=False).count()
     
     # Parámetro de ordenamiento desde la URL
     order_by = request.GET.get('order_by', 'id_personalizado')  # Default order by id
     
     # Filtrar órdenes de trabajo que no están terminadas y ordenarlas
     ordenes = OrdenTrabajo.objects.filter(estado=False).order_by(order_by)
     
      # Paginación
     paginator = Paginator(ordenes, 15)  # Mostrar 15 órdenes por página
     page_number = request.GET.get('page')
     ordenes_page = paginator.get_page(page_number)

     ordenes = OrdenTrabajo.objects.filter(estado=False)
     context={
          'notificaciones': notificaciones,
          'notificaciones_no_leidas': notificaciones_no_leidas,
          'ordenes':ordenes,
          'ordenes_page': ordenes_page, # Usar ordenes_page en lugar de ordenes
     }
     return render(request, 'accounts/ordenes/ordenes.html', context)