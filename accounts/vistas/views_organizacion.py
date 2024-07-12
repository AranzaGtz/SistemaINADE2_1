# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import TerminosForm
from accounts.models import Formato


def terminos_avisos(request):
    formato = get_object_or_404(Formato, id=3)
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