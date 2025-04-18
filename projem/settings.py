
from decouple import config
from pathlib import Path
from django.contrib.messages import constants as messages
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  
    'django.contrib.staticfiles',
    'libraryapp',
    'account',
    'django_recaptcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
              BASE_DIR / 'templates',  
            BASE_DIR / 'libraryapp' / 'templates', 
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

WSGI_APPLICATION = 'projem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True


SESSION_COOKIE_AGE = 24 * 60 * 60  # 24 saat (saniye cinsinden)
SESSION_SAVE_EVERY_REQUEST = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_ROOT = BASE_DIR /"staticfiles"
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_URL = '/media/'  # Tarayıcıda dosyalar /media/ ile erişilecek
MEDIA_ROOT = BASE_DIR / 'media'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/account/login"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-info",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

SITE_URL = 'http://127.0.0.1:8000'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP sunucu adresi (Gmail örneği)
EMAIL_PORT = 587  # Port (587, TLS için yaygın olarak kullanılır)
EMAIL_USE_TLS = True  # TLS bağlantısı kullanmak için True yapın
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # E-posta adresiniz
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # E-posta şifreniz
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Varsayılan gönderen e-posta
SECRET_KEY = config('DJANGO_SECRET_KEY')
GOOGLE_BOOKS_API_KEY = config('GOOGLE_BOOKS_API_KEY', default='')
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')
HUGGINGFACE_TOKEN = config('HUGGINGFACE_TOKEN')
BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
API_URL = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'


# Yerel test için (opsiyonel)
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']




BASE_DIR = Path(__file__).resolve().parent.parent

# Log ayarları
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),  # debug.log dosyasına yazılacak
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'account': {  # account uygulaması için logger
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
