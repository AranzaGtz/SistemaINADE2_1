from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import DireccionForm, EmpresaForm
from accounts.models import Direccion, Empresa, Persona
from django.contrib import messages
from django.core.paginator import Paginator

# VISTA MOSTRAR EMPRESAS
def empresa_cont_list(request):

    # Parámetro de ordenamiento desde la URL
    order_by = request.GET.get('order_by', 'nombre_empresa')  # Orden por defecto
    
    if not order_by:  # Asegura que siempre haya un valor válido para order_by
        order_by = 'nombre_empresa'

    # Obtener todas las empresas y ordenarlas
    empresas = Empresa.objects.all().order_by(order_by)
    
    # Paginación
    paginator = Paginator(empresas, 10)  # Muestra 15 empresas por página
    page_number = request.GET.get('page')
    empresas_page = paginator.get_page(page_number)

    empresa_form = EmpresaForm()

    context = {
        'empresas_page': empresas_page,  # Usar solo empresas_page para la tabla
        'empresa_form': empresa_form
    }
    
    return render(request, "accounts/empresas/empresas.html", context)


# VISTA CREAR EMPRESA EN MODAL
def empresa_create(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            # Crear o actualizar la dirección
            direccion, created = Direccion.objects.update_or_create(
                calle=form.cleaned_data['calle'],
                numero=form.cleaned_data['numero'],
                colonia=form.cleaned_data['colonia'],
                ciudad=form.cleaned_data['ciudad'],
                codigo=form.cleaned_data['codigo'],
                estado=form.cleaned_data['estado'],
            )
            
            # Crear o actualizar la empresa
            empresa = form.save(commit=False)
            empresa.direccion = direccion
            empresa.save()

            return redirect('empresas_cont_list')
    else:
        form = EmpresaForm()

    return render(request, 'accounts/empresas/empresas.html', {'form': form})

# VISTA EDITAR EMPRESAS
def empresa_edit(request, pk):
    empresa = get_object_or_404(Empresa,id=pk)
    direccion = empresa.direccion
    
    empresa_form = EmpresaForm(instance=empresa)
    direccion_form = DireccionForm(instance=direccion)
    
    empresas = Empresa.objects.all()
    
    return render(request, "accounts/empresas/empresas_editar.html",{
        "empresa":empresa,
        "empresas":empresas,
        "empresa_form":empresa_form,
        "direccion_form":direccion_form
        })
    
# VISTA ACTUALIZAR EMPRESAS
def empresa_update(request,pk):
    empresa = get_object_or_404(Empresa,id=pk)
    direccion = empresa.direccion
    
    if request.method=='POST':
        empresa_form = EmpresaForm(request.POST, instance=empresa)
        direccion_form = DireccionForm(request.POST, instance=direccion)
        
        if empresa_form.is_valid() and direccion_form.is_valid():
            direccion = direccion_form.save()
            empresa = empresa_form.save(commit=False)
            empresa.direccion = direccion
            empresa.save()
            messages.success(request, 'Empresa actualizada!.')
            return redirect("empresas_cont_list")
    else:
        empresa_form = EmpresaForm(instance=empresa)
        direccion_form = DireccionForm(instance=direccion)
    return redirect(request, "empresas_cont_list",{
        "empresa":empresa,
        "empresa_form":empresa_form,
        "direccion_form":direccion_form,
        })

# VISTA PARA ELIMINAR EMPRESA
def empresa_delete(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    if request.method == "POST":
        empresa.delete()
        messages.success(request, 'Emrpesa Eliminada!.')
        # Redirigir a la lista de empresas después de la eliminación
        return redirect('empresas_cont_list')
    return render(request, 'accounts/empresas/eliminar_empresa.html', {'empresa': empresa})
