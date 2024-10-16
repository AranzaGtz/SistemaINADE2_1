from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from accounts.models import CustomUser, OrdenTrabajo, OrdenTrabajoConcepto
from django.core.paginator import Paginator


#    VISTA PARA ORDENES DE TRABAJO
def ordenes_list(request):
    # Parámetro de ordenamiento desde la URL
    order_by = request.GET.get('order_by', 'id_personalizado')  # Default order by id_personalizado
    order_direction = request.GET.get('order_direction', 'desc')  # Dirección ascendente o descendente, por defecto ascendente

    if not order_by:  # Asegura que siempre haya un valor válido para order_by
        order_by = 'id_personalizado'

    # Si la dirección es descendente, se agrega el prefijo '-'
    if order_direction == 'desc':
        order_by = f'-{order_by}'

    # Filtrar órdenes de trabajo que no están terminadas y ordenarlas
    ordenes = OrdenTrabajo.objects.filter(estado=False).order_by(order_by)

    # Paginación
    paginator = Paginator(ordenes, 10)  # Mostrar 10 órdenes por página
    page_number = request.GET.get('page')
    ordenes_page = paginator.get_page(page_number)

    context = {
        'ordenes': ordenes,
        'ordenes_page': ordenes_page,  # Usar ordenes_page en lugar de ordenes
    }
    return render(request, 'accounts/ordenes/ordenes.html', context)


#    VISTA PARA DETALLES DE UNA ORDEN DE TRABAJO
def detalle_orden_trabajo(request, id_personalizado):
    
     orden_trabajo = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
     conceptos = OrdenTrabajoConcepto.objects.filter(orden_de_trabajo=orden_trabajo.id_personalizado)

     context = {
          'orden_trabajo': orden_trabajo,
          'conceptos': conceptos,
     }
     return render(request, 'accounts/ordenes/orden_detalle.html', context) 
     
#    VISTA PARA VER ARCHIVO PDF ORDEN DE TRABAJO
def orden_trabajo_pdf(request, id_personalizado):
     try:
          orden_trabajo = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
          # Verificar si el archivo PDF existe
          if OrdenTrabajo.orden_trabajo_pdf:
               # Retornar el archivo PDF guardado
               return FileResponse(orden_trabajo.orden_trabajo_pdf.open(), content_type='application/pdf')
          else:
               raise Http404("El archivo PDF no se encuentra.")
     except FileNotFoundError:
          raise Http404("El archivo PDF no se encuentra disponible.")
     