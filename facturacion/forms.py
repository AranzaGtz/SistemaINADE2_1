import re
from django import forms
from .models import CSD

#    FORMULARIO PARA CARGAR INFORMACIÓN PARA CSD O SELLO DIGITAL
class CSDForm(forms.ModelForm):
     password = forms.CharField(
          widget=forms.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'passwordHelpBlock'}), label="Contraseña del CSD")

     class Meta:
          model = CSD
          # Especifica los campos del formulario
          fields = ['rfc', 'cer_file', 'key_file', 'password']
          widgets = {
               'rfc': forms.TextInput(attrs={'class': 'form-control'}),
               'cer_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'formCerFile'}),
               'key_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'formKeyFile'}),
               'password': forms.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'passwordHelpBlock'}),
          }
          labels = {
               'rfc': 'RFC',
               'cer_file': 'Archivo .cer',
               'key_file': 'Archivo .key',
          }
     
     def clean_rfc(self):
          rfc = self.cleaned_data.get('rfc').strip().upper()

          # Validar RFC (Formato estándar: 4 letras + 6 dígitos + 3 caracteres)
          rfc_regex = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$')
          if not rfc_regex.match(rfc):
               raise forms.ValidationError('Por favor, ingresa un RFC válido.')

          return rfc
          
     def clean_cer_file(self):
          cer_file = self.cleaned_data.get('cer_file')
          
          if cer_file:
               # Verificar si el archivo tiene la extensión .cer
               if not cer_file.name.endswith('.cer'):
                    raise forms.ValidationError('El archivo debe tener la extensión .cer.')

          return cer_file
     
     def clean_key_file(self):
          key_file = self.cleaned_data.get('key_file')
          
          if key_file:
               # Verificar si el archivo tiene la extensión .key
               if not key_file.name.endswith('.key'):
                    raise forms.ValidationError('El archivo debe tener la extensión .key.')

          return key_file

