from django import forms
from maestro.models import Clase, Grupo          # Solo importa lo que está en maestro/models.py
from core.models import Asistencia, Perfil, Progreso, Nivel  # El resto modelos y perfil vienen de core

# Elimina el import: from .models import Asistencia, Alumno
# Si necesitas algún "Alumno", usa Perfil y filtrado por rol.

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['alumno', 'presente']
        widgets = {
            'alumno': forms.HiddenInput(),  # normalmente el alumno viene del contexto
        }

class MarcarAsistenciaForm(forms.Form):
    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    presente = forms.BooleanField(required=False)

class ProgresoForm(forms.ModelForm):
    class Meta:
        model = Progreso
        fields = ['alumno', 'nivel', 'comentarios', 'completado']
        widgets = {
            'alumno': forms.HiddenInput(),
            'comentarios': forms.Textarea(attrs={'rows':3}),
        }

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['grupo', 'fecha', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical;'}),
        }
