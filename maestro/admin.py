from django.contrib import admin
from .models import Grupo

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'descripcion')  # Cambié 'maestro' por 'profesor'
    list_filter = ('profesor',)  # También cambiado aquí si lo tenías
    search_fields = ('nombre', 'descripcion', 'profesor__user__username')
    filter_horizontal = ('alumnos',)  # Para manejar la relación ManyToMany de alumnos de forma visual

    def get_queryset(self, request):
        # Optimiza las consultas para evitar N+1 queries
        return super().get_queryset(request).select_related('profesor__user')
