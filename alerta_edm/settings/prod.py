from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
