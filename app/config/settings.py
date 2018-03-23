"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# melon/app을 가리킴
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Static
# User-uploaded file들이 저장될 위치
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'
# 프로젝트 정적파일들을 검색({% static %})할 디렉토리 목록
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_URL = '/static/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'members.User'
# Application definition

# YOUTUBE_API_KEY = 'AIzaSyAXcxxlOahgGS3Jo0SINkbn8B_Uof5qHWE'

# FACEBOOK_SECRET_CODE = 'faa6f7d8ce69fa9b63e2a8ebba8b3a4e'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.FacebookBackend',
    'members.backends.APIFacebookBackend',
]



# SECRET #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')

# 1) base.json 파일을 읽어온 결과
f = open(SECRETS_BASE, 'rt')
base_text = f.read()
f.close()

# 2) 위 결과(JSON형식의 문자열)를 파이선 객체로 변환
secrets_base = json.loads(base_text)

# print(secrets_base)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets_base['SECRET_KEY']
YOUTUBE_API_KEY = secrets_base['YOUTUBE_API_KEY']
FACEBOOK_APP_ID = secrets_base['FACEBOOK_APP_ID']
FACEBOOK_SECRET_CODE = secrets_base['FACEBOOK_SECRET_CODE']
EMAIL_HOST_PASSWORD = secrets_base['EMAIL_HOST_PASSWORD']
SMS_API_KEY = secrets_base['SMS_API_KEY']
SMS_API_SECRET = secrets_base['SMS_API_SECRET']
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *





REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}




# django-cors-headers
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '0.0.0.0:3000',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',

    'album',
    'artist',
    'members',
    'song',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # 장고가 템플릿 파일을 검색할 경로 목록
            TEMPLATE_DIR,
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'fc-melon',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'USER': 'fc-7th',
#         'PASSWORD': 'dlgksdud',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
        # 'NAME': 'fc-melon',
        # 'USER': 'smallbee3',
        # 'PASSWORD': 'asdfqwer',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
