from django.urls import path
from . import views

app_name = 'core'  # 

urlpatterns = [
    path('', views.home, name='home'),
    path('subir-documentos/', views.subir_documentos, name='subir_documentos'),
    path('registrar-pago/', views.registrar_pago, name='registrar_pago'),
    path('progreso/', views.progreso_alumno, name='progreso'),
]
