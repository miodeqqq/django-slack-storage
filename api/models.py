# -*- coding: utf-8 -*-

import os

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from solo.models import SingletonModel
from tinymce.models import HTMLField


def slack_user_files_directory(instance, filename):
    """
    Upload path for files in SlackUsers model.
    """

    file_name, ext = os.path.splitext(filename)

    return os.path.join('posted_by_users_files/{file_name}{ext}'.format(
        file_name=slugify(file_name),
        ext=ext
    ))


class SlackConfiguration(SingletonModel):
    """
    Model to store Slack configuration data.
    """

    api_token = models.CharField(
        'API Token',
        max_length=150,
        unique=True
    )

    class Meta:
        verbose_name = 'Slack config'
        verbose_name_plural = 'Slack config'


class SlackChannels(models.Model):
    """
    Model to store Slack channels.
    """

    channel_name = models.CharField(
        'Channel name',
        blank=True,
        null=True,
        max_length=100,
    )

    channel_id = models.CharField(
        'Channel ID',
        blank=True,
        null=True,
        max_length=20,
    )

    channel_description = models.TextField(
        'Channel description',
        blank=True,
        null=True

    )

    members = models.TextField(
        'Channel members',
        blank=True,
        null=True
    )

    number_of_members = models.IntegerField(
        'Number of members',
        default=0,
    )

    def __str__(self):
        return self.channel_name

    class Meta:
        verbose_name = 'Slack channel'
        verbose_name_plural = 'Slack channels'


class SlackUsers(models.Model):
    """
    Model to store Slack users.
    """

    slack_id = models.CharField(
        'Slack ID',
        max_length=32,
        blank=True,
        null=True
    )

    slack_username = models.CharField(
        'Username',
        blank=True,
        null=True,
        max_length=255
    )

    slack_email = models.CharField(
        'Email',
        max_length=255,
        blank=True,
        null=True
    )

    slack_avatar_path = models.URLField(
        'Avatar URL',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.slack_username if self.slack_username else self.slack_email

    class Meta:
        verbose_name = 'Slack user'
        verbose_name_plural = 'Slack users'


class SlackMessages(models.Model):
    """
    General model to store messages from channels.
    """

    channel_name = models.CharField(
        'Channel name',
        max_length=255,
        blank=True,
        null=True,
    )

    message = HTMLField(
        'Message',
        blank=True,
        null=True,
    )

    author_of_message = models.CharField(
        'User',
        blank=True,
        null=True,
        max_length=255
    )

    timestamp = models.DateTimeField(
        'Timestamp'
    )

    def clean(self):
        super(SlackMessages, self).clean()

        already_exists = self.__class__.objects.filter(
            message=self.message,
            author_of_message=self.author_of_message,
            timestamp=self.timestamp
        ).count()

        if already_exists > 0:
            raise ValidationError(
                'Duplicate!'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(SlackMessages, self).save(*args, **kwargs)

    def __str__(self):
        return self.channel_name

    class Meta:
        verbose_name = 'Slack message'
        verbose_name_plural = 'Slack messages'


class SlackFiles(models.Model):
    """
    General model to store urls to posted files and its author.
    """

    user = models.CharField(
        'Slack user',
        blank=True,
        null=True,
        max_length=255
    )

    file_path = models.URLField(
        'File path',
    )

    user_file = models.FileField(
        'Slack user\'s file',
        upload_to=slack_user_files_directory,
        db_index=True,
        blank=True,
        null=True
    )

    download_status = models.BooleanField(
        'Download status',
        default=False,
        db_index=True
    )

    timestamp = models.DateTimeField(
        'Timestamp'
    )

    class Meta:
        verbose_name = 'Slack user file'
        verbose_name_plural = 'Slack users files'

    def __str__(self):
        return self.user


class SlackPrivateChannels(models.Model):
    """
    Model to store private Slack channels.
    """

    private_channel_name = models.CharField(
        'Private channel name',
        blank=True,
        null=True,
        max_length=100,
    )

    private_channel_id = models.CharField(
        'Private channel ID',
        blank=True,
        null=True,
        max_length=20,
    )

    private_channel_creator = models.CharField(
        'Private channel creator',
        blank=True,
        null=True,
        max_length=100
    )

    private_channel_members = models.TextField(
        'Private channel members',
        blank=True,
        null=True
    )

    private_channel_value = models.TextField(
        'Private channel value',
        blank=True,
        null=True
    )

    private_channel_topic = models.CharField(
        'Private channel topic',
        blank=True,
        null=True,
        max_length=255
    )

    def __str__(self):
        return self.private_channel_name

    class Meta:
        verbose_name = 'Slack private channel'
        verbose_name_plural = 'Slack private channels'


class SlackTeamEmojis(models.Model):
    """
    General model to store Slack team's emojis.
    """

    emoji = models.CharField(
        'Emoji',
        blank=True,
        null=True,
        max_length=64
    )

    emoji_path = models.CharField(
        'Emoji path',
        blank=True,
        null=True,
        max_length=255
    )

    class Meta:
        verbose_name = 'Slack emoji'
        verbose_name_plural = 'Slack emojis'

    def __str__(self):
        return self.emoji
