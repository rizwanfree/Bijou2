from pathlib import Path
# import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables

# env = environ.Env()
# environ.Env.read_env(BASE_DIR / ".env")

# Retrieve the values from the environment
# AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME')
# AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY')
# AZURE_CONTAINER = env('AZURE_CONTAINER')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j)6wou66he6+p*b=c3hv=crphr&)%y4y+333til0try7uu2paa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'storages',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    
    'mainweb',
    'accomodations',
    'finances',
    
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

ROOT_URLCONF = 'BijouDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'BijouDjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

    # 'default': {
    #     'ENGINE': 'mssql',
    #     'NAME': 'Vuetesting',
    #     'USER': 'rizwanadmincodecraft',
    #     'PASSWORD': 'Aspire$112',
    #     'HOST': 'codecraftsolutions.database.windows.net',
    #     'PORT': 1433,
    #     'OPTIONS': {
    #         'driver': 'ODBC Driver 17 for SQL Server',
    #         'extra_params': 'schema=dj_testing;',  # Use your test schema here                        
    #         'extra_params': 'Encrypt=yes;TrustServerCertificate=no',
    #     },
    # }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/




# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'https://baijotest-e5becebbd9byawbh.uaenorth-01.azurewebsites.net'
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


MEDIA_URL = '/media/'
MEDIA_ROOT = [BASE_DIR / 'media']

# STORAGES = {
#     # Store static files locally (CSS, JS, images)
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },

#     # Store uploaded media files in Azure
#     "default": {
#         "BACKEND": "storages.backends.azure_storage.AzureStorage",
#     }
# }


LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'mainweb:index'
LOGIN_REDIRECT_URL = 'mainweb:index'


#DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"
