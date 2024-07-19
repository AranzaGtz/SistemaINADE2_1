from django.shortcuts import redirect, render, get_object_or_404
from django.db.models.deletion import ProtectedError
from accounts.forms import MetodoForm, ServicioForm
from accounts.models import Metodo, Servicio
from django.contrib import messages

# VISTA PARA DIRIGIR A INTERFAZ DE SERVICIOS
def servicios_list(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    context = {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'servicios' : Servicio.objects.all(),
        'metodos' : Metodo.objects.all(),
        'metodo_form' : MetodoForm(),
        'servicio_form': ServicioForm()
    }
    return render(request,'accounts/servicios/servicios.html',context)

# VISTA PARA CREAR UN SERVICIO
def servicio_create(request):
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST)
        metodo_form = MetodoForm(request.POST) if 'crear_metodo_checkbox' in request.POST else None

        if servicio_form.is_valid():
            if 'crear_metodo_checkbox' in request.POST:
                if metodo_form and metodo_form.is_valid():
                    metodo = metodo_form.save()
                else:
                    messages.error(request, 'Por favor, corrige los errores en el formulario de método.')
                    return render(request, 'accounts/servicios/servicios.html', {
                        'servicio_form': servicio_form,
                        'metodo_form': metodo_form,
                        'metodos': Metodo.objects.all(),
                    })
            elif 'metodo' in request.POST and request.POST['metodo']:
                metodo = Metodo.objects.get(id=request.POST['metodo'])
            else:
                messages.error(request, 'Por favor, selecciona o crea un método.')
                return render(request, 'accounts/servicios/servicios.html', {
                    'servicio_form': servicio_form,
                    'metodo_form': metodo_form,
                    'metodos': Metodo.objects.all(),
                })

            # Crear el servicio
            servicio = servicio_form.save(commit=False)
            servicio.metodo = metodo
            servicio.save()

            messages.success(request, 'Servicio creado con éxito')
            return redirect('servicios_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        servicio_form = ServicioForm()
        metodo_form = MetodoForm()

    metodos = Metodo.objects.all()
    context = {
        'servicio_form': servicio_form,
        'metodo_form': metodo_form,
        'metodos': metodos,
    }
    return render(request, 'accounts/servicios/servicios.html', context)

# VISTA PARA EDITAR UN SERVICIO
def servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, id=pk)

    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)

        if servicio_form.is_valid():
            metodo_id = request.POST.get('metodo')
            if metodo_id:
                metodo = get_object_or_404(Metodo, pk=metodo_id)
                servicio = servicio_form.save(commit=False)
                servicio.metodo = metodo
                servicio.save()
                messages.success(request, 'Servicio actualizado con éxito.')
                return redirect('servicios_list')
            else:
                messages.error(request, 'Por favor, selecciona un método.')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')

    else:
        servicio_form = ServicioForm(instance=servicio)

    context = {
        'servicio_form': servicio_form,
        'servicio': servicio,
        'metodos': Metodo.objects.all(),
    }
    return render(request, 'accounts/servicios/servicios_editar.html', context)

# Vista para eliminar un servicio
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        try:
            servicio.delete()
            messages.success(request, 'Servicio eliminado con éxito.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el servicio porque está siendo referenciado por otros registros.')
        return redirect('servicios_list')

# VISTA PARA BORRAR METODO
def metodo_create(request):
    if request.method == 'POST':
        form = MetodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Metodo agregado!.')
            return redirect('servicios_list')
    else:
        context = {
            'form' : MetodoForm()
        }
    return render(request, 'servicios_list', context)

# VISTA PARA ELIMINAR METODOS
def metodo_delete(request,pk):
    metodo = Metodo.objects.get(id = pk)
    metodo.delete()
    messages.success(request, 'Metodo eliminado!.')
    return redirect('servicios_list')
