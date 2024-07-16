# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import OrganizacionForm, TerminosForm
from accounts.models import Formato, Organizacion

#   VISTA PARTA ACTUALIZAR TERMINOS Y AVISOS
def terminos_avisos(request):
    formato = Formato.objects.first()
    if not formato:
        # Si no existe ninguna organización, crea una nueva instancia
        formato = Organizacion()
        formato.save()
    if request.method == 'POST':
        form = TerminosForm(request.POST, instance=formato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terminos actualizados.')
            # Redirige a la vista deseada después de guardar
            return redirect('home')
    else:
        form = TerminosForm(instance=formato)
   
    return render(request, 'accounts/organizacion/terminos.html',{'form':form})

#   VISTA PARA ACTUALIZAR LA ORGANIZACIÓN
def editar_organizacion(request):
    organizacion = Organizacion.objects.first()
    if not organizacion:
        # Si no existe ninguna organización, crea una nueva instancia
        organizacion = Organizacion()
        organizacion.save()

    if request.method == 'POST':
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página de inicio o a la página adecuada
    else:
        form = OrganizacionForm(instance=organizacion)

    return render(request, 'accounts/organizacion/editar_organizacion.html', {'form': form})