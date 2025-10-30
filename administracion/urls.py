from django.urls import path
from . import views

app_name = 'administracion'
urlpatterns = [
    path('login/', views.login_admin, name='login'), 
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('panel/', views.panel_usuarios, name='panel_usuarios'),

    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('eliminar-usuario/<int:perfil_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('asignar-alumnos/<int:grupo_id>/', views.asignar_alumnos_grupo, name='asignar_alumnos_grupo'),
    path('subir-documento/<int:grupo_id>/', views.subir_documento, name='subir_documento'),
    path('documentos-grupo/<int:grupo_id>/', views.documentos_grupo, name='documentos_grupo'),
    path('supervision-reportes/', views.supervision_reportes, name='supervision_reportes'),
    path('validar-documentos/', views.validar_documentos, name='validar_documentos'),
    path('validar-doc/<int:doc_id>/<str:tipo_doc>/<str:accion>/', views.validar_estado_documento, name='validar_estado_documento'),
    path('crear-grupo/', views.crear_grupo, name='crear_grupo'),
    path('asignar-profesor/<int:grupo_id>/', views.asignar_profesor_grupo, name='asignar_profesor_grupo'),
    path('editar-usuario/<int:perfil_id>/', views.editar_usuario, name='editar_usuario'),
    path('editar-grupo/<int:grupo_id>/', views.editar_grupo, name='editar_grupo'),
    path('eliminar-grupo/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('eliminar-documento/<int:doc_id>/', views.eliminar_documento, name='eliminar_documento'),
    path('crear-pago/', views.crear_pago, name='crear_pago'),
    path('eliminar-pago/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
    path('validar-pago/<int:pago_id>/', views.validar_pago, name='validar_pago'),
    path('rechazar-pago/<int:pago_id>/', views.rechazar_pago, name='rechazar_pago'),
    path('pagos/', views.pagos_admin, name='pagos_admin'),
    path('clases/', views.clases_admin, name='clases'),

]
