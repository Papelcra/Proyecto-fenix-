from django.contrib import admin
from .models import Perfil, Documento, Nivel, Membresia, Pago, Asistencia, Progreso

# 🔹 Registramos todos los modelos para que aparezcan en el panel de admin
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono', 'direccion')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'rol')
    list_filter = ('rol',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha_subida')
    search_fields = ('alumno__user__username',)

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')

@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_dias')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'membresia', 'fecha_pago', 'valor', 'estado')
    list_filter = ('estado',)

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'alumno', 'fecha', 'presente')
    list_filter = ('presente', 'fecha')

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'nivel', 'completado')
    list_filter = ('completado', 'nivel')
