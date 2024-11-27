import os
from pathlib import Path
import environ

# Construir rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializar environ para variables de entorno
env = environ.Env(
    DEBUG=(bool, False),  # Valor por defecto para DEBUG es False
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost'])  # Hosts permitidos por defecto
)

# Leer el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# CONFIGURACIONES DE SEGURIDAD
DEBUG = 'RENDER' not in os.environ

# Desactivar todas las configuraciones de seguridad en desarrollo
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Las demás configuraciones de seguridad
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['*'] if DEBUG else [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Esto permitirá todos los subdominios de onrender.com
]
# Configuración de logging para ver más detalles
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Definición de aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps propias
    'aplicaciones.home',  
    'aplicaciones.usuarios',  
    'aplicaciones.reservations',
    'aplicaciones.rooms',
]

# Configuración de archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = '/static/'  # URL para acceder a archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directorio para collectstatic
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Directorios adicionales para archivos estáticos

# Configuración de archivos de media (archivos subidos por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Middleware de la aplicación
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Para internacionalización
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs raíz
ROOT_URLCONF = 'proyectoReservas.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Directorio general de templates
            os.path.join(BASE_DIR, 'aplicaciones/home/templates'),  # Templates específicos de home
        ],
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

# Aplicación WSGI
WSGI_APPLICATION = 'proyectoReservas.wsgi.application'

# Configuración de la base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={env("DB_SCHEMA")}'
        }
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Configuraciones de internacionalización
LANGUAGE_CODE = 'es-ar'  # Código de idioma para español de Argentina
TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Zona horaria de Buenos Aires
USE_I18N = True  # Habilitar internacionalización
USE_TZ = True  # Habilitar manejo de zona horaria

# Campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de autenticación
AUTH_USER_MODEL = 'usuarios.CustomUser'  # Modelo personalizado de usuario
LOGIN_URL = '/usuarios/iniciar-sesion/'  # URL de inicio de sesión
LOGIN_REDIRECT_URL = '/reservations/'  # URL después de iniciar sesión


# Configuración para manejo de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 semanas en segundos
SESSION_COOKIE_NAME = 'sessionid'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False

# Configuraciones adicionales de seguridad para producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'