# /accounts/views_prospectos.py

from django.db import IntegrityError, transaction
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import ConceptoFormSet, CotizacionForm, DireccionForm, EmpresaForm, InformacionContactoForm, ProspectoForm, PersonaForm
from django.contrib import messages
from accounts.models import Persona, Prospecto, Titulo
from django.db.models import Q

# VISTA PARA DIRIGIR A INTERFAZ DE PROSPECTOS

def prospecto_list(request):
    search_query = request.GET.get('search', '')
    
    # Inicializar la consulta de prospectos
    prospectos = Prospecto.objects.all()
    
    # Filtrar por términos de búsqueda
    if search_query:
        prospectos = prospectos.filter(
            Q(persona__titulo__icontains=search_query) |
            Q(persona__nombre__icontains=search_query) |
            Q(persona__apellidos__icontains=search_query) |
            Q(persona__empresa__nombre_empresa__icontains=search_query) |
            Q(persona__informacion_contacto__correo_electronico__icontains=search_query)
        )
    
    return render(request, "accounts/prospectos/prospectos.html", {'prospectos': prospectos})

# VISTA PARA REDIRIJIR A prospecto_create
def prospecto_new(request):
    direccion_form = DireccionForm()
    empresa_form = EmpresaForm()
    persona_form = PersonaForm()
    informacion_contacto_form = InformacionContactoForm()
    prospecto_form = ProspectoForm()
    return render(request, "accounts/prospectos/prospecto_crear.html", {
        'direccion_form': direccion_form,
        'empresa_form': empresa_form,
        'persona_form': persona_form,
        'informacion_contacto_form': informacion_contacto_form,
        'prospecto_form': prospecto_form
    })

# VISTA PARA REGISTRAR PROSPECTOS
def prospecto_create(request): 
    
    if request.method == 'POST':
        direccion_form = DireccionForm(request.POST)
        empresa_form = EmpresaForm(request.POST)
        contacto_form = InformacionContactoForm(request.POST)
        persona_form = PersonaForm(request.POST)
        prospecto_form = ProspectoForm(request.POST)
        

        if direccion_form.is_valid() and empresa_form.is_valid() and contacto_form.is_valid():
            direccion = direccion_form.save()
            empresa = empresa_form.save(commit=False)
            empresa.direccion = direccion
            empresa.save()

            contacto = contacto_form.save()
            
            persona = persona_form.save(commit=False)
            persona.empresa = empresa
            persona.informacion_contacto = contacto
            persona.save()
            
            prospecto = Prospecto.objects.create(persona=persona)
            
            messages.success(request, 'Usuario registrado!.')
            return redirect('prospecto_list')
        else:
            print("Direccion form errors:", direccion_form.errors)
            print("Empresa form errors:", empresa_form.errors)
            print("Contacto form errors:", contacto_form.errors)
            print("Persona form errors:", persona_form.errors)
            print("Prospecto form errors:", prospecto_form.errors)
    else:
        direccion_form = DireccionForm()
        empresa_form = EmpresaForm()
        contacto_form = InformacionContactoForm()
        persona_form = PersonaForm()
        prospecto_form = ProspectoForm()

    return render(request, 'accounts/prospectos/prospectos.html', {
        'direccion_form': direccion_form,
        'empresa_form': empresa_form,
        'contacto_form': contacto_form,
        'persona_form': persona_form,
        'prospecto_form': prospecto_form
    })

# VISTA PARA RENDERIZAR A FORMULARIO LOS PROSPECTOS
def prospecto_edit(request,pk):
    prospecto = get_object_or_404(Prospecto,id=pk)
    informacion_contacto = prospecto.persona.informacion_contacto
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
def prospecto_update(request, pk):
    prospecto = get_object_or_404(Persona, id=pk)
    
    if request.method == 'POST':
        prospecto_form = PersonaForm(request.POST, instance=prospecto)
        
        if prospecto_form.is_valid():
            prospecto_form.save()
            messages.success(request, 'Usuario actualizado!.')
            return redirect('prospecto_list')
    else:
        prospecto_form = PersonaForm(instance=prospecto)

    return render(request, "accounts/prospectos/prospecto_editar.html", {
        "prospecto": prospecto,
        "prospecto_form": prospecto_form,
        "edit": True
    })
    
# VISTA PARA ELIMINAR PROSPECTO
def prospecto_delete(request,pk):
    prospecto = Prospecto.objects.get(id = pk)
    informacion_contacto = prospecto.persona.informacion_contacto
    informacion_contacto.delete()
    prospecto.delete()
    messages.success(request, '¡Usuario eliminado!.')
    return redirect('prospecto_list')

# AGREGAR NUEVA COTIZACION DESDE PROSPECTOS
def cotizacion_form_con_cliente(request,persona_id, moneda):
    persona = get_object_or_404(Persona, id=persona_id)
    cotizacion_form = CotizacionForm(initial={'persona': persona, 'metodo_pago': moneda})
    concepto_formset = ConceptoFormSet()
    
    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })