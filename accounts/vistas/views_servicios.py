from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import MetodoForm, ServicioForm
from accounts.models import Metodo, Servicio
from django.contrib import messages

# VISTA PARA DIRIGIR A INTERFAZ DE SERVICIOS
def servicios_list(request):
    context = {
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
        metodo_form = MetodoForm(request.POST)

        if servicio_form.is_valid():
            servicio = servicio_form.save(commit=False)
            servicio.metodo_id = request.POST.get('metodo')
            servicio.save()
            messages.success(request, 'Servicio registrado!.')
            return redirect('servicios_list') 
    else:
        metodo_form = MetodoForm()
        servicio_form = ServicioForm()
    
    context = {
        'servicio_form': servicio_form,
        'metodo_form': metodo_form,
    }
    return render(request, 'accounts/servicios/servicios.html', context)

# VISTA PARA EDITAR UN SERVICIO
def servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        if servicio_form.is_valid():
            servicio_form.save()
            
            messages.success(request, 'Servicio registrado!.')
            return redirect('servicios_list')
    else:
        servicio_form = ServicioForm(instance=servicio)
        metodo_form = MetodoForm()

    return render(request, 'accounts/servicios/servicios_editar.html', {
        'servicio_form': servicio_form,
        'metodo_form': metodo_form,
        'metodos': Metodo.objects.all(),
        'servicio': servicio,
    })

# VISTA PARA ACTUALIZAR UN SERVICIO
def servicio_update(request, pk):
    servicio = get_object_or_404(Servicio, id=pk)
    metodo = servicio.metodo
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        
        if 'metodo' in request.POST and request.POST['metodo'] == 'nuevo':
            metodo_form = MetodoForm(request.POST)
            if metodo_form.is_valid():
                metodo = metodo_form.save()
                servicio.metodo = metodo
        else:
            metodo_id = request.POST.get('metodo')
            if metodo_id:
                metodo = get_object_or_404(Metodo, id=metodo_id)
                servicio.metodo = metodo
        
        if servicio_form.is_valid():
            servicio_form.save()
            messages.success(request, 'Servicio actualizado!')
            return redirect('servicios_list')
    else:
        servicio_form = ServicioForm(instance=servicio)
        metodo_form = MetodoForm(instance=metodo)

    return render(request, 'accounts/servicios/servicios_editar.html', {
        'servicio_form': servicio_form,
        'metodo_form': metodo_form,
        'metodos': Metodo.objects.all(),
        'servicio': servicio,
    })

# Vista para eliminar un servicio
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    servicio.delete()
    messages.success(request, 'Servicio eliminado exitosamente!')
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
