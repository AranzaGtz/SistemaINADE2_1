# views_personas.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.forms import DireccionForm, EmpresaForm, PersonaForm, TituloForm
from accounts.models import Empresa, Persona, InformacionContacto, Titulo
from django.core.paginator import Paginator

# VISTA PARA CREAR TITULO
def agregar_titulo(request):
    if request.method == 'POST':
        form = TituloForm(request.POST)
        if form.is_valid():
            titulo = form.save()
            # Devuelve un script para cerrar la ventana y actualizar el campo select
            return HttpResponse(f"""
                <script>
                    window.opener.actualizarSelectTitulo({{ id: {titulo.id}, titulo: '{titulo.titulo}' }});
                    window.close();
                </script>
            """)
    else:
        form = TituloForm()

    return render(request, 'accounts/clientes/agregar_titulo.html', {'form': form})

# VISTA PARA CERRAR VENTAS
def cerrar_ventana(request):
    return HttpResponse('<script>window.close();</script>')

def obtener_titulos(request):
    titulos = Titulo.objects.all().values('id', 'titulo')
    return JsonResponse(list(titulos), safe=False)

# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
def lista_clientes(request):

    # Parámetro de ordenamiento desde la URL
    # Ordena por 'id' como predeterminado
    order_by = request.GET.get('order_by', 'id')
    
    if not order_by:  # Asegura que siempre haya un valor válido para order_by
        order_by = 'id'

    # Obtiene todas las personas activas y las ordena
    personas = Persona.objects.all().filter(activo=True).order_by(order_by)
    p= personas.count
    # Obtiene todas las personas activas y las ordena
    personas_no_activas = Persona.objects.all().filter(activo=False).order_by(order_by)

    # Paginación
    paginator = Paginator(personas, 50)  # Muestra 50 personas por página
    page_number = request.GET.get('page')
    personas_page = paginator.get_page(page_number)

    # Obtiene todos los títulos y empresas
    titulos = Titulo.objects.all()
    empresas = Empresa.objects.all()

    # Formularios vacíos
    persona_form = PersonaForm()
    empresa_form = EmpresaForm()

    # Contexto que se pasa a la plantilla
    context = {
        'personas_page': personas_page,
        'titulos': titulos,
        'empresas': empresas,
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'personas_no_activas': personas_no_activas,
        'p':p,
        'p2':personas_no_activas.count
    }

    return render(request, 'accounts/clientes/clientes.html', context)

# VISTA PARA CREAR CLIENTES DESDE MODAL
def cliente_create(request):
    if request.method == 'POST':
        # Crea formularios con los datos enviados por el usuario
        action = request.POST.get('action', 'create')
        persona_form = PersonaForm(request.POST)
        empresa_form = EmpresaForm(
            request.POST) if 'crear_empresa_checkbox' in request.POST else None
        direccion_form = DireccionForm(
            request.POST) if 'crear_empresa_checkbox' in request.POST else None

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
                    messages.error(
                        request, 'Por favor, corrige los errores en el formulario de empresa.')
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
                messages.error(
                    request, 'Por favor, selecciona o crea una empresa.')
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

            if action == 'create_and_quote':
                messages.success(request, "El cliente ha sido creado!")
                return redirect('cotizacion_form', persona_id=persona.id)
                
            else:
                messages.success(request, "El cliente ha sido creado!")
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
            messages.success(request, "El cliente se actualizo correctamente!")
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
    # Desactiva el cliente
    cliente.activo = False
    cliente.save()
    # Muestra un mensaje de éxito y redirige a la lista de clientes
    messages.success(request, 'Cliente desactivado con éxito.')
    return redirect('lista_clientes')