from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import MetodoForm, ServicioForm
from accounts.models import Metodo, Servicio

def metodos_list(request):
    metodos = Metodo.objects.all()
    return render(request,'accounts/servicios/servicios_metodos.html', {'metodos': metodos})

def metodo_create(request):
    if request.method == 'POST':
        form = MetodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('metodos_list')
    else:
        form = MetodoForm()
    return render(request, 'metodo_form.html', {'form': form})

# VISTA PARA ELIMINAR METODOS
def metodo_delete(request,pk):
    metodo = Metodo.objects.get(id = pk)
    metodo.delete()
    messages.success(request, 'Metodo eliminado exitosamente!.')
    return redirect('metodos_list')

# VISTA PARA DIRIGIR A INTERFAZ DE SERVICIOS
def servicios_list(request):
    servicios = Servicio.objects.all()
    return render(request,'accounts/servicios/dashboard_admin_servicios.html',{'servicios':servicios})

# VISTA PARA CREAR UN SERVICIO
def servicio_new(request):
    metodo_form = MetodoForm()
    servicio_form = ServicioForm()
    lista_metodos = Metodo.objects.all()
    return render(request, "accounts/servicios/servicios_crear.html", {'metodo_form': metodo_form, 'servicio_form': servicio_form, 'metodos': lista_metodos})

# VISTA PARA CREAR UN SERVICIO
def servicio_create(request):
    if request.method == 'POST':
        if 'metodo' in request.POST and request.POST['metodo'] == 'nuevo':
            metodo_form = MetodoForm(request.POST)
            servicio_form = ServicioForm(request.POST)
            if metodo_form.is_valid() and servicio_form.is_valid():
                nuevo_metodo = metodo_form.save()
                servicio = servicio_form.save(commit=False)
                servicio.metodo = nuevo_metodo
                servicio.save()
                return redirect('servicios_list')
        else:
            servicio_form = ServicioForm(request.POST)
            if servicio_form.is_valid():
                servicio = servicio_form.save(commit=False)
                servicio.metodo_id = request.POST.get('metodo')
                servicio.save()
                return redirect('servicios_list')
    else:
        metodo_form = MetodoForm()
        servicio_form = ServicioForm()
    
    metodos = Metodo.objects.all()
    return render(request, 'accounts/servicios/dashboard_admin_servicios.html', {
        'metodo_form': metodo_form,
        'servicio_form': servicio_form,
        'metodos': metodos
    })

# VISTA PARA EDITAR UN SERVICIO
def servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        if servicio_form.is_valid():
            servicio_form.save()
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
            messages.success(request, 'Servicio actualizado exitosamente!')
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