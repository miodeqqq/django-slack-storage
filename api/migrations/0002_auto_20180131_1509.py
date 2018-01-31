# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
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
            name='file_content_type',
            field=models.CharField(verbose_name='Content-Type', max_length=255, blank=True, db_index=True),
        ),
        migrations.AddField(
            model_name='slackfiles',
            name='file_sha256_checksum',
            field=models.CharField(verbose_name='SHA-256', max_length=255, blank=True, db_index=True),
        ),
        migrations.AddField(
            model_name='slackfiles',
            name='file_size',
            field=models.PositiveIntegerField(verbose_name='File size', db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='slackfiles',
            name='user_file',
            field=models.FileField(verbose_name="Slack user's file", blank=True, null=True, db_index=True, upload_to=api.models.slack_user_files_directory),
        ),
        migrations.AlterField(
            model_name='slackchannels',
            name='channel_description',
            field=models.TextField(verbose_name='Channel description', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackchannels',
            name='channel_id',
            field=models.CharField(verbose_name='Channel ID', max_length=20, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackchannels',
            name='channel_name',
            field=models.CharField(verbose_name='Channel name', max_length=100, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackchannels',
            name='members',
            field=models.TextField(verbose_name='Channel members', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackchannels',
            name='number_of_members',
            field=models.IntegerField(verbose_name='Number of members', db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='slackfiles',
            name='user',
            field=models.CharField(verbose_name='Slack user', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackmessages',
            name='author_of_message',
            field=models.CharField(verbose_name='User', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackmessages',
            name='channel_name',
            field=models.CharField(verbose_name='Channel name', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackmessages',
            name='message',
            field=tinymce.models.HTMLField(verbose_name='Message', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_creator',
            field=models.CharField(verbose_name='Private channel creator', max_length=100, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_id',
            field=models.CharField(verbose_name='Private channel ID', max_length=20, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_members',
            field=models.TextField(verbose_name='Private channel members', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_name',
            field=models.CharField(verbose_name='Private channel name', max_length=100, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_topic',
            field=models.CharField(verbose_name='Private channel topic', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackprivatechannels',
            name='private_channel_value',
            field=models.TextField(verbose_name='Private channel value', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackteamemojis',
            name='emoji',
            field=models.CharField(verbose_name='Emoji', max_length=64, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackteamemojis',
            name='emoji_path',
            field=models.CharField(verbose_name='Emoji path', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackusers',
            name='slack_avatar_path',
            field=models.URLField(verbose_name='Avatar URL', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackusers',
            name='slack_email',
            field=models.CharField(verbose_name='Email', max_length=255, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackusers',
            name='slack_id',
            field=models.CharField(verbose_name='Slack ID', max_length=32, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='slackusers',
            name='slack_username',
            field=models.CharField(verbose_name='Username', max_length=255, blank=True, null=True, db_index=True),
        ),
    ]
