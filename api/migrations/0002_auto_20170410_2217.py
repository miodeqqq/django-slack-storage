# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackfiles',
            name='download_status',
            field=models.BooleanField(verbose_name='Download status', db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='slackfiles',
            name='user_file',
            field=models.FileField(verbose_name="Slack user's file", blank=True, null=True, db_index=True, upload_to=api.models.slack_user_files_directory),
        ),
    ]
