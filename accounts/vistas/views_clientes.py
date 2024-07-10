# views_personas.py

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.forms import DireccionForm, EmpresaForm, PersonaForm
from accounts.models import Empresa, Persona, InformacionContacto, Titulo

# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
def lista_clientes(request):
    # Obtiene todas las personas activas
    personas = Persona.objects.filter(activo=True)
    # Obtiene todos los títulos
    titulos = Titulo.objects.all()
    # Obtiene todas las empresas
    empresas = Empresa.objects.all()
    # Crea un formulario vacío de Persona
    persona_form = PersonaForm()
    # Crea un formulario vacío de Empresa
    empresa_form = EmpresaForm()
    
    # Contexto que se pasa a la plantilla
    context = {
        'personas': personas,
        'titulos': titulos,
        'empresas': empresas,
        'persona_form': persona_form,
        'empresa_form': empresa_form
    }
    
    # Renderiza la plantilla de clientes con el contexto
    return render(request, 'accounts/clientes/clientes.html', context)

# VISTA PARA CREAR CLIENTES DESDE MODAL
def cliente_create(request):
    if request.method == 'POST':
        # Crea formularios con los datos enviados por el usuario
        persona_form = PersonaForm(request.POST)
        empresa_form = EmpresaForm(request.POST) if 'crear_empresa_checkbox' in request.POST else None
        direccion_form = DireccionForm(request.POST) if 'crear_empresa_checkbox' in request.POST else None

        if persona_form.is_valid():
            # Guarda la información de contacto primero
            informacion_contacto = InformacionContacto(
                correo_electronico=persona_form.cleaned_data['correo_electronico'],
                telefono=persona_form.cleaned_data['telefono'],
                celular=persona_form.cleaned_data['celular'],
                fax=persona_form.cleaned_data['fax']
            )
            informacion_contacto.save()

            # Comprueba si se seleccionó una empresa existente o se necesita crear una nueva
            if 'crear_empresa_checkbox' in request.POST:
                if empresa_form and empresa_form.is_valid() and direccion_form and direccion_form.is_valid():
                    direccion = direccion_form.save()
                    empresa = empresa_form.save(commit=False)
                    empresa.direccion = direccion
                    empresa.save()
                else:
                    # Si hay errores en los formularios, muestra un mensaje de error y renderiza la plantilla con los formularios
                    messages.error(request, 'Por favor, corrige los errores en el formulario de empresa.')
                    return render(request, 'accounts/clientes/clientes.html', {
                        'persona_form': persona_form,
                        'empresa_form': empresa_form,
                        'direccion_form': direccion_form,
                        'empresas': Empresa.objects.all(),
                        'titulos': Titulo.objects.all()
                    })
            elif 'empresa' in request.POST and request.POST['empresa']:
                # Obtiene la empresa seleccionada
                empresa = Empresa.objects.get(id=request.POST['empresa'])
            else:
                # Si no se selecciona ni crea una empresa, muestra un mensaje de error
                messages.error(request, 'Por favor, selecciona o crea una empresa.')
                return render(request, 'accounts/clientes/clientes.html', {
                    'persona_form': persona_form,
                    'empresa_form': empresa_form,
                    'empresas': Empresa.objects.all(),
                    'titulos': Titulo.objects.all()
                })

            # Crea el cliente
            persona = persona_form.save(commit=False)
            persona.empresa = empresa
            persona.informacion_contacto = informacion_contacto
            persona.save()

            # Muestra un mensaje de éxito y redirige a la lista de clientes
            messages.success(request, 'Cliente creado con éxito')
            return redirect('lista_clientes')
        else:
            # Si hay errores en el formulario de persona, muestra un mensaje de error
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        # Si no es un POST, crea formularios vacíos
        persona_form = PersonaForm()
        empresa_form = EmpresaForm()
        direccion_form = DireccionForm()

    # Obtiene todos los títulos
    titulos = Titulo.objects.all()
    # Contexto que se pasa a la plantilla
    context = {
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'direccion_form': direccion_form,
        'empresas': Empresa.objects.all(),
        'titulos': titulos,
    }
    
    # Renderiza la plantilla de clientes con el contexto
    return render(request, 'accounts/clientes/clientes.html', context)

# VISTA PARA EDITAR CLIENTE
def cliente_edit(request, pk):
    # Obtiene la persona por su ID o muestra un 404 si no se encuentra
    persona = get_object_or_404(Persona, id=pk)
    informacion_contacto = persona.informacion_contacto

    if request.method == 'POST':
        # Crea un formulario con los datos enviados y la instancia de persona
        persona_form = PersonaForm(request.POST, instance=persona)
        if persona_form.is_valid():
            # Actualiza la información de contacto
            informacion_contacto.correo_electronico = persona_form.cleaned_data['correo_electronico']
            informacion_contacto.telefono = persona_form.cleaned_data['telefono']
            informacion_contacto.celular = persona_form.cleaned_data['celular']
            informacion_contacto.fax = persona_form.cleaned_data['fax']
            informacion_contacto.save()

            # Guarda la persona
            persona_form.save()
            # Muestra un mensaje de éxito y redirige a la lista de clientes
            messages.success(request, 'Cliente actualizado con éxito')
            return redirect('lista_clientes')
    else:
        # Si no es un POST, inicializa el formulario con los datos actuales de la persona
        initial_data = {
            'correo_electronico': informacion_contacto.correo_electronico,
            'telefono': informacion_contacto.telefono,
            'celular': informacion_contacto.celular,
            'fax': informacion_contacto.fax,
        }
        persona_form = PersonaForm(instance=persona, initial=initial_data)

    # Contexto que se pasa a la plantilla
    context = {
        'persona_form': persona_form,
        'persona': persona,
    }
    
    # Renderiza la plantilla de edición de cliente con el contexto
    return render(request, 'accounts/clientes/editar_cliente.html', context)

# VISTA PARA ELIMINAR CLIENTES
def cliente_delete(request, pk):
    # Obtiene el cliente por su ID o muestra un 404 si no se encuentra
    cliente = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        # Desactiva el cliente
        cliente.activo = False
        cliente.save()
        # Muestra un mensaje de éxito y redirige a la lista de clientes
        messages.success(request, 'Cliente desactivado con éxito.')
        return redirect('lista_clientes')
    
    # Renderiza la plantilla de eliminación de cliente con el contexto
    return render(request, 'accounts/clientes/eliminar_cliente.html', {'cliente': cliente})
