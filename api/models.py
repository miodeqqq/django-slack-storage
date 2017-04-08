# -*- coding: utf-8 -*-

from django.db import models
from solo.models import SingletonModel
from tinymce.models import HTMLField

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