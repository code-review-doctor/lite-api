import json
import os
import sys

from environ import Env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env(
    ALLOWED_HOSTS=(str, ''),
    DEBUG=(bool, False),
    LOG_LEVEL=(str, 'INFO'),
    BACKGROUND_TASK_ENABLED=(bool, False),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = env('DEBUG')

# Please use this to Enable/Disable the Admin site
ADMIN_ENABLED = True

ALLOWED_HOSTS = json.loads(env('ALLOWED_HOSTS')) if env('ALLOWED_HOSTS') else []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'addresses',
    'applications.apps.ApplicationsConfig',
    'organisations.apps.OrganisationsConfig',
    'users.apps.UsersConfig',
    'cases.apps.CasesConfig',
    'applications.drafts.apps.DraftsConfig',
    'goods.apps.GoodsConfig',
    'parties.apps.PartiesConfig',
    'teams.apps.TeamsConfig',
    'queues.apps.QueuesConfig',
    'gov_users',
    'static',
    'static.control_list_entries',
    'static.countries',
    'static.units',
    'static.denial_reasons',
    'static.statuses',
    'reversion',
    'drf_yasg',
    'content_strings.apps.ContentStringsConfig',
    'goodstype',
    'flags.apps.FlagsConfig',
    'documents.apps.DocumentsConfig',
    'background_task',
    'picklists',
    'parties.document',
    'queries',
    'queries.end_user_advisories',
    'queries.control_list_classifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'conf.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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

AUTH_USER_MODEL = "users.BaseUser"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
    ),
    'DEFAULT_PERMISSION_CLASSES': (
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'conf.wsgi.application'

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'conf.urls.api_info',
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    }
else:
    DATABASES = {
        'default': env.db()
    }

S3_CLIENT = 'boto3'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_REGION = env('AWS_REGION')
S3_DOWNLOAD_LINK_EXPIRY_SECONDS = 180

AV_SERVICE_URL = env('AV_SERVICE_URL')
AV_SERVICE_USERNAME = env('AV_SERVICE_USERNAME')
AV_SERVICE_PASSWORD = env('AV_SERVICE_PASSWORD')

BACKGROUND_TASK_ENABLED = env('BACKGROUND_TASK_ENABLED')

# If True, print the length of time it takes to run each test
TIME_TESTS = True

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if 'test' not in sys.argv:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '(asctime)(levelname)(message)(filename)(lineno)(threadName)(name)(thread)(created)(process)(processName)(relativeCreated)(module)(funcName)(levelno)(msecs)(pathname)', # noqa
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': env('LOG_LEVEL').upper(),
            },
        }
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
    }

ADMIN_TEAM_ID = '00000000-0000-0000-0000-000000000001'
