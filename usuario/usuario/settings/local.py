from .base import *


import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',   # Puedes cambiar esto según tu configuración de PostgreSQL
        'PORT': '5432',        # Puedes cambiar esto según tu configuración de PostgreSQL
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# en la base del proyecto se reconocera static para guardar archivos estaticos
STATICFILES_DIRS = [
    str(BASE_DIR/'static'),
]


# Configuracion para cargar imagenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# condiguracion de envio de email con gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = get_secret('EMAIL')
EMAIL_HOST_PASSWORD = get_secret('PASSWORD_EMAIL')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
