
"""
Django settings for charity_site project.
"""

from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0h0brem7sc9#s6@p^2-&$#lv#o#n0k#sd$72(yoslq67p!p%&i')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Разрешаем наш домен и локальные адреса
ALLOWED_HOSTS = ['aragats-antar.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']

# Application definition
INSTALLED_APPS = [
    'cloudinary',
    'cloudinary_storage',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main', 

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'charity_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'charity_site.wsgi.application'

# Database (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Yerevan'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('hy', 'Հայերեն'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main', 'static'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Настройки Cloudinary
import cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# Хранилища (ТОЛЬКО через STORAGES для Django 5.1)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# КРИТИЧЕСКИ ВАЖНО: Отключаем строгую проверку манифеста
WHITENOISE_MANIFEST_STRICT = False

# ЯДЕРНАЯ МЕРА: Запрещаем WhiteNoise сжимать JS-файлы, 
# чтобы ошибка с fi.js больше никогда не возникала при сборке.
# Статика будет работать, просто без gzip-сжатия JS (разница незаметна).
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ('.js',)

MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'