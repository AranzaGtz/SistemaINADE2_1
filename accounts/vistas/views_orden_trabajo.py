from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from accounts.models import OrdenTrabajo, OrdenTrabajoConcepto
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

#    VISTA PARA DETALLES DE UNA ORDEN DE TRABAJO
def detalle_orden_trabajo(request, id_personalizado):
     # Notificación
     notificaciones = request.user.notificacion_set.all()
     notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
     orden_trabajo = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
     conceptos = OrdenTrabajoConcepto.objects.filter(orden_de_trabajo=orden_trabajo.id_personalizado)
     
     context = {
          'notificaciones': notificaciones,
          'notificaciones_no_leidas': notificaciones_no_leidas,
          'orden_trabajo': orden_trabajo,
          'conceptos': conceptos,
     }
     return render(request, 'accounts/ordenes/orden_detalle.html', context) 
     
#    VISTA PARA VER ARCHIVO PDF ORDEN DE TRABAJO
def orden_trabajo_pdf(request, id_personalizado):
     orden_trabajo = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
     # Verificar si el archivo PDF existe
     if OrdenTrabajo.orden_trabajo_pdf:
          # Retornar el archivo PDF guardado
          return FileResponse(orden_trabajo.orden_trabajo_pdf.open(), content_type='application/pdf')
     else:
          raise Http404("El archivo PDF no se encuentra.")