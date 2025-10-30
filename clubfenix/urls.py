from django.contrib import admin
from django.urls import path, include

# 🔹 IMPORTAR LA CONFIGURACIÓN DE MEDIA PARA SERVIR ARCHIVOS EN DESARROLLO
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Logout vía Django auth_views
    path('logout/', include('django.contrib.auth.urls')),  # usa template registration/logged_out.html

    # Apps
    path('', include('inicio.urls')),                      # index y login personalizados
    path('maestro/', include(('maestro.urls', 'maestro'), namespace='maestro')),
    path('administracion/', include(('administracion.urls', 'administracion'), namespace='administracion')),
    path('alumno/', include(('alumno.urls', 'alumno'), namespace='alumno')),
    path('core/', include('core.urls')),                   # si tienes urls en core
]

# 🔹 Solo en DEVELOPMENT: servir archivos de la carpeta documentos/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
