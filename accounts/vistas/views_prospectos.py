# /accounts/views_prospectos.py
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import ConceptoFormSet, CotizacionForm, DireccionForm, EmpresaForm, InformacionContactoForm, ProspectoForm, PersonaForm
from django.contrib import messages
from accounts.models import Empresa, InformacionContacto, Persona, Prospecto, Titulo

# VISTA PARA DIRIGIR A INTERFAZ DE PROSPECTOS
def prospecto_list(request):
    prospectos = Prospecto.objects.all()
    titulos = Titulo.objects.all()
    empresas = Empresa.objects.all()
    persona_form = PersonaForm()
    empresa_form = EmpresaForm()
    prospecto_from = ProspectoForm()
    context ={
        'prospectos':prospectos,
        'titulos': titulos,
        'empresas':empresas,
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'prospecto_form': prospecto_from
    }
    return render(request, 'accounts/prospectos/prospectos.html', context)

# VISTA PARA CREAR CLIENTES DESDE MODAL
def prospecto_create(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        empresa_form = EmpresaForm(request.POST) if 'crear_empresa_checkbox' in request.POST else None
        direccion_form = DireccionForm(request.POST) if 'crear_empresa_checkbox' in request.POST else None

        if persona_form.is_valid():
            # Guardar la información de contacto primero
            informacion_contacto = InformacionContacto(
                correo_electronico=persona_form.cleaned_data['correo_electronico'],
                telefono=persona_form.cleaned_data['telefono'],
                celular=persona_form.cleaned_data['celular'],
                fax=persona_form.cleaned_data['fax']
            )
            informacion_contacto.save()

            # Comprobar si se seleccionó una empresa existente o se necesita crear una nueva
            if 'crear_empresa_checkbox' in request.POST:
                if empresa_form and empresa_form.is_valid() and direccion_form and direccion_form.is_valid():
                    direccion = direccion_form.save()
                    empresa = empresa_form.save(commit=False)
                    empresa.direccion = direccion
                    empresa.save()
                else:
                    messages.error(request, 'Por favor, corrige los errores en el formulario de empresa.')
                    return render(request, 'accounts/prospectos/prospectos.html', {
                        'persona_form': persona_form,
                        'empresa_form': empresa_form,
                        'direccion_form': direccion_form,
                        'empresas': Empresa.objects.all(),
                        'titulos': Titulo.objects.all()
                    })
            elif 'empresa' in request.POST and request.POST['empresa']:
                empresa = Empresa.objects.get(id=request.POST['empresa'])
            else:
                messages.error(request, 'Por favor, selecciona o crea una empresa.')
                return render(request, 'accounts/prospectos/prospectos.html', {
                    'persona_form': persona_form,
                    'empresa_form': empresa_form,
                    'empresas': Empresa.objects.all(),
                    'titulos': Titulo.objects.all()
                })

            # Crear el cliente
            persona = persona_form.save(commit=False)
            persona.empresa = empresa
            persona.informacion_contacto = informacion_contacto
            persona.save()
            
            # Crear el prospecto
            prospecto = Prospecto(persona=persona)
            prospecto.save()

            messages.success(request, 'Prospecto creado.')
            return redirect('prospecto_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        persona_form = PersonaForm()
        empresa_form = EmpresaForm()
        direccion_form = DireccionForm()

    titulos = Titulo.objects.all()
    context = {
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'direccion_form': direccion_form,
        'empresas': Empresa.objects.all(),
        'titulos': titulos,
    }
    return render(request, 'accounts/prospectos/prospectos.html', context)

# VISTA PARA ELIMINAR PROSPECTO
def prospecto_delete(request,pk):
    prospecto = get_object_or_404(Prospecto, pk=pk)
    persona = prospecto.persona

    if request.method == 'POST':
        # Eliminar el prospecto
        prospecto.delete()

        messages.success(request, 'Prospecto eliminado con éxito.')
        return redirect('prospecto_list')

    return render(request, 'accounts/clientes/eliminar_cliente.html', {'prospecto': prospecto, 'dp':True})


# AGREGAR NUEVA COTIZACION DESDE PROSPECTOS
def cotizacion_form_con_cliente(request,persona_id, moneda):
    persona = get_object_or_404(Persona, id=persona_id)
    cotizacion_form = CotizacionForm(initial={'persona': persona, 'metodo_pago': moneda})
    concepto_formset = ConceptoFormSet()
    
    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })