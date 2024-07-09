# views_personas.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.forms import DireccionForm, EmpresaForm, PersonaForm
from accounts.models import Empresa, Persona, InformacionContacto, Titulo

# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
def lista_clientes(request):
    
    personas = Persona.objects.filter(activo=True)
    titulos = Titulo.objects.all()
    empresas = Empresa.objects.all()
    persona_form = PersonaForm()
    empresa_form = EmpresaForm()
    context ={
        'personas':personas,
        'titulos': titulos,
        'empresas':empresas,
        'persona_form': persona_form,
        'empresa_form': empresa_form
    }
    return render(request, 'accounts/clientes/clientes.html', context)

# VISTA PARA CREAR CLIENTES DESDE MODAL
def cliente_create(request):
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
                    return render(request, 'accounts/clientes/clientes.html', {
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
                return render(request, 'accounts/clientes/clientes.html', {
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

            messages.success(request, 'Cliente creado con éxito')
            return redirect('lista_clientes')
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
    return render(request, 'accounts/clientes/clientes.html', context)

# VISTA PARA EDITAR CLIENTE
def cliente_edit(request, pk):
    persona = get_object_or_404(Persona, id=pk)
    informacion_contacto = persona.informacion_contacto

    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, instance=persona)
        if persona_form.is_valid():
            # Guardar información de contacto
            informacion_contacto.correo_electronico = persona_form.cleaned_data['correo_electronico']
            informacion_contacto.telefono = persona_form.cleaned_data['telefono']
            informacion_contacto.celular = persona_form.cleaned_data['celular']
            informacion_contacto.fax = persona_form.cleaned_data['fax']
            informacion_contacto.save()

            # Guardar persona
            persona_form.save()
            messages.success(request, 'Cliente actualizado con éxito')
            return redirect('lista_clientes')
    else:
        initial_data = {
            'correo_electronico': informacion_contacto.correo_electronico,
            'telefono': informacion_contacto.telefono,
            'celular': informacion_contacto.celular,
            'fax': informacion_contacto.fax,
        }
        persona_form = PersonaForm(instance=persona, initial=initial_data)

    context = {
        'persona_form': persona_form,
        'persona': persona,
    }
    return render(request, 'accounts/clientes/editar_cliente.html', context)

# VISTA PARA ELIMINAR CLIENTES
def cliente_delete(request, pk):
    cliente = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        cliente.activo = False
        cliente.save()
        messages.success(request, 'Cliente desactivado con éxito.')
        return redirect('lista_clientes')
    return render(request, 'accounts/clientes/eliminar_cliente.html', {'cliente': cliente})
