# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
from django.shortcuts import redirect, render

from accounts.forms import ConceptoForm, CotizacionForm, DireccionForm, EmpresaForm, InformacionContactoForm, PersonaForm, ProspectoForm
from accounts.models import Empresa, Persona, Prospecto


def cotizaciones_list (request):
    # Lista_clientes = Empresa.objects.all()
    return render(request, "accounts/cotizaciones/dashboard_admin_cotizaciones.html") #,{"empresas":Lista_clientes}

def cotizacion_new (request):
    context = {
        'persona_form': PersonaForm(),
        'informacion_contacto_form': InformacionContactoForm(),
        'personas': Persona.objects.all(),
        'empresas': Empresa.objects.all(),
        'direccion_form':DireccionForm(),
        'empresa_form': EmpresaForm(),
    }
    return render(request, "accounts/cotizaciones/cotizaciones_crear.html",context)

def cotizacion_register(request):
    if request.method == 'POST':
        persona_id = request.POST.get('persona')
        if persona_id == 'nuevo':
            persona_form = PersonaForm(request.POST)
            informacion_contacto_form = InformacionContactoForm(request.POST)
            if persona_form.is_valid() and informacion_contacto_form.is_valid():
                nueva_persona = persona_form.save()
                nueva_informacion_contacto = informacion_contacto_form.save(commit=False)
                nueva_informacion_contacto.persona = nueva_persona
                nueva_informacion_contacto.save()
                prospecto = Prospecto(persona=nueva_persona)
                prospecto.save()
                # Aquí puedes proceder a crear la cotización con el nuevo prospecto
                return redirect('cotizaciones_list')
        else:
            persona = Persona.objects.get(id=persona_id)
            prospecto, created = Prospecto.objects.get_or_create(persona=persona)
            # Aquí puedes proceder a crear la cotización con el prospecto existente
            return redirect('cotizaciones_list')
    else:
        return render(request, "accounts/cotizaciones/cotizaciones_registro.html")