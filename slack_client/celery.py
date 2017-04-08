# -*- coding: utf-8 -*-

from __future__ import absolute_import

import django
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slack_client.settings')
django.setup()

app = Celery('slack_client')
CELERY_TIMEZONE = 'UTC'
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)