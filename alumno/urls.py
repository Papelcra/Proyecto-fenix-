from django.urls import path
from . import views

app_name = 'alumno'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pagos/', views.pagos, name='pagos'),
    path('progreso/', views.progreso, name='progreso'),
    path('subir-comprobante/<int:pago_id>/', views.subir_comprobante, name='subir_comprobante'),
    path('clases/', views.clases_alumno, name='clases'),
]




