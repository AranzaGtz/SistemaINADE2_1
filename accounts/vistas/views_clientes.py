# views_personas.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from accounts.forms import InformacionContactoForm, PersonaForm
from accounts.models import Persona, InformacionContacto

# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
def lista_clientes(request):
    search_query = request.GET.get('search', '')
    personas = Persona.objects.filter(activo=True)

    if search_query:
        personas = personas.filter(
            Q(titulo__icontains=search_query) |
            Q(nombre__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(empresa__nombre_empresa__icontains=search_query) |
            Q(informacion_contacto__correo_electronico__icontains=search_query)
        )

    return render(request, 'accounts/clientes/clientes.html', {'personas': personas})

# VISTA PARA ELIMINAR CLIENTES
def cliente_delete(request, pk):
    cliente = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        cliente.activo = False
        cliente.save()
        messages.success(request, 'Cliente desactivado con éxito.')
        return redirect('lista_clientes')
    return render(request, 'accounts/clientes/eliminar_cliente.html', {'cliente': cliente})

# VISTA PARA EDITAR CLIENTES
def cliente_edit(request, pk):
    cliente = get_object_or_404(Persona, id=pk)
    contacto = cliente.informacion_contacto
    
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, instance=cliente)
        contacto_form = InformacionContactoForm(request.POST, instance=contacto)
        if persona_form.is_valid() and contacto_form.is_valid():
            contacto_form.save()
            persona_form.save()
            messages.success(request, 'Cliente actualizado con éxito.')
            return redirect('lista_clientes')
    else:
        persona_form = PersonaForm(instance=cliente)
        contacto_form = InformacionContactoForm(instance=contacto)
    
    return render(request, 'accounts/clientes/editar_cliente.html', {
        'persona_form': persona_form,
        'contacto_form': contacto_form,
    })
