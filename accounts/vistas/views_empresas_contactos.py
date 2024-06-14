from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import DireccionForm, EmpresaForm, InformacionContactoForm, ProspectoForm
from accounts.models import Empresa, Prospecto, Titulo
from django.contrib import messages

# VISTA MOSTRAR EMPRESAS
def empresa_cont_list(request):
    empresas = Empresa.objects.all()
    contactos = Prospecto.objects.all()
    return render(request, "accounts/empresas/dashboard_admin_empresas_contactos.html",
        {"empresas": empresas,
        'contactos':contactos})

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
            messages.success(request, 'Empresa actualizada exitosamente!.')
            return redirect("empresas_cont_list")
    else:
        empresa_form = EmpresaForm(instance=empresa)
        direccion_form = DireccionForm(instance=direccion)
    return redirect(request, "empresas_cont_list",{
        "empresa":empresa,
        "empresa_form":empresa_form,
        "direccion_form":direccion_form,
        })

# VISTA ELIMINAR EMPRESAS
def empresa_delete(request,pk):
    empresa = Empresa.objects.get(id = pk)
    direccion = empresa.direccion
    direccion.delete()
    empresa.delete()
    messages.success(request, 'Empresa eliminada exitosamente!.')
    return redirect('empresas_cont_list')

# VISTA EDITAR CONTACTOS
def contacto_edit(request,pk):
    prospecto = get_object_or_404(Prospecto,id=pk)
    informacion_contacto = prospecto.informacion_contacto
    titulos = Titulo.objects.all()
    
    prospecto_form = ProspectoForm(instance=prospecto)
    informacion_contacto_form = InformacionContactoForm(instance=informacion_contacto)
    
    prospectos = Prospecto.objects.all()
    # show_modal = True  # Esta variable indica si la ventana modal debe estar abierta
    return render(request, "accounts/prospectos/prospecto_editar.html",{
        "prospecto":prospecto, 
        "prospectos":prospectos,
        "prospecto_form":prospecto_form,
        "contacto_form":informacion_contacto_form ,
        "titulos":titulos,
        "cont":True})
    
# VISTA ACTUALIZAR CONTACTOS
def contacto_update(request,pk):
    contacto = get_object_or_404(Prospecto,id=pk)
    informacion_contacto = contacto.informacion_contacto
    
    if request.method=='POST':
        contacto_form = ProspectoForm(request.POST, instance=contacto)
        informacion_contacto_form = InformacionContactoForm(request.POST, instance=informacion_contacto)
        
        if contacto_form.is_valid() and informacion_contacto_form.is_valid():
            informacion_contacto = informacion_contacto_form.save()
            contacto = contacto_form.save(commit=False)
            contacto.informacion_contacto = informacion_contacto
            contacto.save()
            messages.success(request, 'Contacto actualizado exitosamente!.')
            return redirect("empresas_cont_list")
    else:
        contacto_form = ProspectoForm(instance=contacto)
        informacion_contacto_form = InformacionContactoForm(instance=informacion_contacto)
    return redirect(request, "empresas_cont_list",{
        "contacto":contacto,
        "contacto_form":contacto_form,
        "informacion_contacto_form":informacion_contacto_form,
        })

# VISTA ELIMINAR CONTACTOS
def contacto_delete(request,pk):
    contacto = Prospecto.objects.get(id = pk)
    informacion_contacto = contacto.informacion_contacto
    informacion_contacto.delete()
    contacto.delete()
    messages.success(request, 'Contacto eliminado exitosamente!.')
    return redirect('empresas_cont_list')
