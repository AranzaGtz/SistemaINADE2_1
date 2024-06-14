# /accounts/views_prospectos.py

from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import DireccionForm, EmpresaForm, InformacionContactoForm, ProspectoForm
from django.contrib import messages
from accounts.models import Prospecto, Titulo


# VISTA PARA DIRIGIR A INTERFAZ DE PROSPECTOS
def prospecto_list(request):
    prospectos = Prospecto.objects.all()
    return render(request, "accounts/prospectos/dashboard_admin_prospectos.html",{'prospectos': prospectos})

# VISTA PARA REDIRIJIR A prospecto_create
def prospecto_new(request):
    return render(request, "accounts/prospectos/prospecto_crear.html")

# VISTA PARA REGISTRAR PROSPECTOS
def prospecto_create(request): 
    
    if request.method == 'POST':
        direccion_form = DireccionForm(request.POST)
        empresa_form = EmpresaForm(request.POST)
        contacto_form = InformacionContactoForm(request.POST)
        prospecto_form = ProspectoForm(request.POST)

        if direccion_form.is_valid() and empresa_form.is_valid() and contacto_form.is_valid():
            direccion = direccion_form.save()
            empresa = empresa_form.save(commit=False)
            empresa.direccion = direccion
            empresa.save()

            contacto = contacto_form.save()
            
            prospecto = prospecto_form.save(commit=False)
            prospecto.empresa = empresa
            prospecto.informacion_contacto = contacto
            prospecto.save()
            
            messages.success(request, 'Usuario registrado exitosamente!.')

            return redirect('prospecto_list')
        else:
            print("Direccion form errors:", direccion_form.errors)
            print("Empresa form errors:", empresa_form.errors)
            print("Contacto form errors:", contacto_form.errors)
            print("Prospecto form errors:", prospecto_form.errors)
    else:
        direccion_form = DireccionForm()
        empresa_form = EmpresaForm()
        contacto_form = InformacionContactoForm()
        prospecto_form = ProspectoForm()

    return render(request, 'accounts/prospectos/dashboard_admin_prospectos.html', {
        'direccion_form': direccion_form,
        'empresa_form': empresa_form,
        'contacto_form': contacto_form,
        'prospecto_form': prospecto_form
    })

# VISTA PARA RENDERIZAR A FORMULARIO LOS PROSPECTOS
def prospecto_edit(request,pk):
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
        "titulos":titulos,})
    
# VISTA PARA EDITAR EL REGISTRO DE PROSPECTO
def prospecto_update(request,pk):
    prospecto=get_object_or_404(Prospecto,id=pk)
    infromacion_contacto = prospecto.informacion_contacto
    
    if request.method=='POST':
        prospecto_form = ProspectoForm(request.POST, instance=prospecto)
        infromacion_contacto_form = InformacionContactoForm(request.POST, instance=infromacion_contacto)
        
        if prospecto_form.is_valid() and infromacion_contacto_form.is_valid():
            informacion_contacto = infromacion_contacto_form.save()
            prospecto = prospecto_form.save(commit=False)
            prospecto.informacion_contacto = informacion_contacto
            prospecto.save()
            messages.success(request, '¡Usuario actualizado exitosamente!.')
            return redirect("prospecto_list")
    else:
        prospecto_form = ProspectoForm(instance=prospecto)
        informacion_contacto_form = InformacionContactoForm(instance=informacion_contacto)
    return redirect(request, "prospecto_list",{
        "prospecto":prospecto,
        "prospecto_form":prospecto_form,
        "contacto_form":informacion_contacto_form,
        "edit":True
        })
    
# VISTA PARA ELIMINAR PROSPECTO
def prospecto_delete(request,pk):
    prospecto = Prospecto.objects.get(id = pk)
    informacion_contacto = prospecto.informacion_contacto
    informacion_contacto.delete()
    prospecto.delete()
    messages.success(request, '¡Usuario eliminado exitosamente!.')
    return redirect('prospecto_list')