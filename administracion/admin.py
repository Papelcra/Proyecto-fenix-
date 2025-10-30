from django.contrib import admin
from .models import Pago, Documento

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'monto', 'fecha_pago', 'descripcion')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'archivo', 'descripcion')
