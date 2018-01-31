# -*- coding: utf-8 -*-

import os

from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'd-#ti38-if235@353j!$8u!9^r(%=_w#gmbpt)zdyirn!5u)iz'

DEBUG = False

ALLOWED_HOSTS = ['*']

DEFAULT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'api',
)

THIRD_PARTY_APPS = (
    'suit',
    'django.contrib.admin',
    'solo',
    'djcelery',
    'tinymce',
    'django_extensions'
)

INSTALLED_APPS = DEFAULT_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'slack_client.urls'

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

WSGI_APPLICATION = 'slack_client.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Django Slack Storage v1.1.0',

    'MENU': (
        '-',
        {'app': 'api', 'label': 'Slack Storage', 'icon': 'icon-folder-open', 'models': (
            (
                'slackconfiguration',
                'slackchannels',
                'slackprivatechannels',
                'slackusers',
                'slackmessages',
                'slackfiles',
                'slackteamemojis'
            )
        )},
        '-',
    ),
}

CELERY_IMPORTS = [
    'api.tasks',
]

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

RABBIT_HOSTNAME = 'rabbitmq'
BROKER_CONNECTION_TIMEOUT = 10
BROKER_POOL_LIMIT = 1
BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
    user='guest',
    password='guest',
    hostname=RABBIT_HOSTNAME,
    vhost=''
)

BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}

BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

CELERYBEAT_SCHEDULE = {}

CELERYBEAT_API = {
    'get_slack_users_task': {
        'task': 'get_slack_users_task',
        'schedule': crontab(minute='*/5')
    },
    'get_slack_channels_task': {
        'task': 'get_slack_channels_task',
        'schedule': crontab(minute='*/10')
    },
    'get_channel_messages_task': {
        'task': 'get_channel_messages_task',
        'schedule': crontab(minute='*/10')
    },
    'get_posted_by_users_files_task': {
        'task': 'get_posted_by_users_files_task',
        'schedule': crontab(minute='*/10')
    },
    'get_slack_private_channels_task': {
        'task': 'get_slack_private_channels_task',
        'schedule': crontab(minute='*/30')
    },
    'get_team_emojis_task': {
        'task': 'get_team_emojis_task',
        'schedule': crontab(hour='*/12')
    },
    'download_posted_by_users_files_task': {
        'task': 'download_posted_by_users_files_task',
        'schedule': crontab(minute='*/10')
    },
}

CELERYBEAT_SCHEDULE.update(CELERYBEAT_API)

NOTEBOOK_ARGUMENTS = [
    '--ip=0.0.0.0',
    '--port=8888',
    '--no-browser',
    '--NotebookApp.password="sha1:74181c6846fc:16307b9757974c1b9b3796c637b00340c450548c"'
]
