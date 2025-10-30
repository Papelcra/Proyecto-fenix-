from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# 🔹 BASE_DIR con Pathlib 
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-*b7$(qnh=jjaq^z%+f5$dsx_h&_imof@@2f5*71uyu@#23+d^t'
DEBUG = True
ALLOWED_HOSTS = []

# 🔹 APPS INSTALADAS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'core',
    'inicio',
    'eventos',
    'administracion',
    'maestro', 
    'alumno',
]

# 🔹 MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clubfenix.urls'

# 🔹 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ✅ Solo una definición de DIRS, limpia
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clubfenix.wsgi.application'

# 🔹 BASE DE DATOS (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'club_fenix',
        'USER': 'root',
        'PASSWORD': '1014',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 🔹 VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🔹 INTERNACIONALIZACIÓN
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# 🔹 ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 🔹 CLAVE PRIMARIA POR DEFECTO
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔹 CONFIGURACIÓN DE LOGIN / LOGOUT
LOGIN_URL = '/login/'                 # página de login si no está autenticado
LOGIN_REDIRECT_URL = '/'              # ignorado, usamos nuestra lógica en index
LOGOUT_REDIRECT_URL = '/'
MEDIA_URL = '/documentos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'documentos')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')