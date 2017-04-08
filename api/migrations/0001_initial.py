# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackChannels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('channel_name', models.CharField(verbose_name='Channel name', max_length=100, unique=True, blank=True, null=True)),
                ('channel_id', models.CharField(verbose_name='Channel ID', max_length=20, unique=True, blank=True, null=True)),
                ('channel_description', models.TextField(verbose_name='Channel description', blank=True, null=True)),
                ('members', models.TextField(verbose_name='Channel members', blank=True, null=True)),
                ('number_of_members', models.IntegerField(verbose_name='Number of members', default=0)),
            ],
            options={
                'verbose_name': 'Slack channel',
                'verbose_name_plural': 'Slack channels',
            },
        ),
        migrations.CreateModel(
            name='SlackConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('api_token', models.CharField(verbose_name='API Token', max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Slack config',
                'verbose_name_plural': 'Slack config',
            },
        ),
        migrations.CreateModel(
            name='SlackFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user', models.CharField(verbose_name='Slack user', max_length=255, blank=True, null=True)),
                ('file_path', models.URLField(verbose_name='File path')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
            ],
            options={
                'verbose_name': 'Slack user file',
                'verbose_name_plural': 'Slack users files',
            },
        ),
        migrations.CreateModel(
            name='SlackMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('channel_name', models.CharField(verbose_name='Channel name', max_length=255, blank=True, null=True)),
                ('message', tinymce.models.HTMLField(verbose_name='Message', blank=True, null=True)),
                ('author_of_message', models.CharField(verbose_name='User', max_length=255, blank=True, null=True)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
            ],
            options={
                'verbose_name': 'Slack message',
                'verbose_name_plural': 'Slack messages',
            },
        ),
        migrations.CreateModel(
            name='SlackUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slack_id', models.CharField(verbose_name='Slack ID', max_length=32, blank=True, null=True)),
                ('slack_username', models.CharField(verbose_name='Username', max_length=255, blank=True, null=True)),
                ('slack_email', models.CharField(verbose_name='Email', max_length=255, blank=True, null=True)),
                ('slack_avatar_path', models.URLField(verbose_name='Avatar URL', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Slack user',
                'verbose_name_plural': 'Slack users',
            },
        ),
    ]
