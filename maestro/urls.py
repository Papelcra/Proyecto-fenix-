from django.urls import path
from . import views

app_name = 'maestro'  # importante para usar {% url 'maestro:nombre_path' %} en templates

urlpatterns = [
    # Dashboard principal del profesor
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_maestro, name='login'),

    # Lista de alumnos de un grupo
    path('grupo/<int:grupo_id>/alumnos/', views.alumnos_por_grupo, name='alumnos_por_grupo'),

    # Ver asistencias de un alumno (requiere alumno_id y grupo_id)
    path('alumno/<int:alumno_id>/<int:grupo_id>/asistencias/', views.ver_asistencias_alumno, name='ver_asistencias_alumno'),

    # Reporte general de un grupo
    path('grupo/<int:grupo_id>/reporte/', views.reporte_grupo, name='reporte_grupo'),

    path('grupo/<int:grupo_id>/asistencia/', views.registrar_asistencia_grupo, name='registrar_asistencia_grupo'),
    path('grupo/<int:grupo_id>/alumno/<int:alumno_id>/progreso/', views.editar_progreso_alumno, name='editar_progreso_alumno'),

    path('clases/', views.listar_clases, name='listar_clases'),
    path('crear-clase/', views.crear_clase, name='crear_clase'),

]
