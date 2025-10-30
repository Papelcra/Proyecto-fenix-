from django import forms
from .models import Pago

class PagoAdminForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['alumno', 'monto', 'descripcion']

class ComprobanteForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['comprobante']
