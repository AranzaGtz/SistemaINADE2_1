from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from accounts.models import Cotizacion
from accounts.forms import ConceptoForm

class FormsetCotizacion(FormView):
     template_name = 'accounts/cotizaciones/cotizaciones_registro.html'
     form_class = ConceptoForm
     success_url = reverse_lazy('accounts:cotizaciones_list')