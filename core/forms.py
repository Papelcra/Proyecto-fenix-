from django import forms
from .models import Documento, Pago, Asistencia, Progreso

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['cedula', 'eps', 'autorizacion']


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['membresia', 'valor']


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['alumno', 'presente', 'observacion']


class ProgresoForm(forms.ModelForm):
    class Meta:
        model = Progreso
        fields = ['nivel', 'comentarios', 'completado']
