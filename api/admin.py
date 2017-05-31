# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin

from api.models import SlackConfiguration, SlackChannels, SlackMessages
from api.models import SlackUsers, SlackFiles, SlackPrivateChannels, SlackTeamEmojis


@admin.register(SlackTeamEmojis)
class SlackTeamEmojisAdmin(admin.ModelAdmin):
    fields = (
        'emoji',
        'emoji_path',
    )

    search_fields = (
        'emoji',
    )

    ordering = (
        'emoji',
    )

    list_display = (
        'emoji',
        'get_emoji_as_thumbnail',
    )

    readonly_fields = (
        'emoji',
        'emoji_path',
    )

    list_per_page = 60

    def get_emoji_as_thumbnail(self, obj):
        if obj.emoji_path:
            return mark_safe('<img class="img-responsive" src="{emoji_path}" width="60" height="60" />'.format(
                emoji_path=obj.emoji_path
            ))

        return 'No emoji found'

    get_emoji_as_thumbnail.allow_tags = True
    get_emoji_as_thumbnail.short_description = 'Emojis as thumbnail'


@admin.register(SlackPrivateChannels)
class SlackPrivateChannelsAdmin(admin.ModelAdmin):
    fields = (
        'private_channel_id',
        'private_channel_name',
        'private_channel_creator',
        'private_channel_members',
        'private_channel_value',
        'private_channel_topic',
    )

    search_fields = (
        'private_channel_id',
        'private_channel_name',
        'private_channel_members',
        'private_channel_creator',
    )

    readonly_fields = (
        'private_channel_id',
        'private_channel_name',
        'private_channel_creator',
        'private_channel_members',
        'private_channel_value',
        'private_channel_topic',
    )

    list_filter = (
        'private_channel_creator',
    )

    list_display = (
        'private_channel_id',
        'private_channel_name',
        'private_channel_creator',
        'private_channel_value',
        'private_channel_topic',
    )

    ordering = (
        'private_channel_name',
    )

    list_per_page = 60


@admin.register(SlackFiles)
class SlackFilesAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'user_file',
        'file_path',
        'download_status',
        'timestamp'
    )

    list_display = (
        'user',
        'user_file',
        'download_status',
        'get_file_path_as_url',
        'timestamp'
    )

    list_filter = (
        'user',
    )

    ordering = (
        '-timestamp',
    )

    search_fields = (
        'user',
    )

    readonly_fields = (
        'user',
        'file_path',
        'download_status',
        'timestamp'
    )

    list_per_page = 60

    def get_file_path_as_url(self, obj):
        if obj.file_path:
            return format_html('<a href="{file_path}" target="_blank">{file_path}</a>'.format(
                file_path=obj.file_path
            ))

        return 'No URL.'

    get_file_path_as_url.allow_tags = True
    get_file_path_as_url.short_description = 'File URL'


@admin.register(SlackConfiguration)
class SlackConfigurationAdmin(SingletonModelAdmin):
    fieldsets = [
        (u'Token', {
            'fields': [
                'api_token',
            ]
        }),
    ]


@admin.register(SlackChannels)
class SlackChannelsAdmin(admin.ModelAdmin):
    fields = (
        'channel_name',
        'channel_id',
        'number_of_members',
        'channel_description',
        'members'
    )

    search_fields = (
        'channel_id',
        'channel_name'
    )

    readonly_fields = (
        'channel_id',
        'channel_name',
        'members',
        'number_of_members',
        'channel_description',
    )

    list_display = (
        'channel_id',
        'channel_name',
        'number_of_members',
        'channel_description'
    )

    ordering = (
        'channel_name',
    )

    list_per_page = 60


@admin.register(SlackMessages)
class SlackMessagesAdmin(admin.ModelAdmin):
    fields = (
        'channel_name',
        'author_of_message',
        'message',
        'timestamp'
    )

    search_fields = (
        'channel_name',
        'author_of_message',
    )

    list_display = (
        'channel_name',
        'author_of_message',
        'message',
        'timestamp'
    )

    list_filter = (
        'channel_name',
        'author_of_message'
    )

    readonly_fields = (
        'channel_name',
        'author_of_message',
        'message',
        'timestamp'
    )

    ordering = (
        '-timestamp',
    )

    list_per_page = 60


@admin.register(SlackUsers)
class SlackUsersAdmin(admin.ModelAdmin):
    fields = (
        'slack_id',
        'slack_username',
        'slack_email',
        'slack_avatar_path',
    )

    search_fields = (
        'slack_email',
        'slack_id',
        'slack_username',
    )

    ordering = (
        'slack_username',
    )

    list_display = (
        'slack_username',
        'slack_email',
        'get_avatar_as_thumbnail'
    )

    readonly_fields = (
        'slack_id',
        'slack_username',
        'slack_email',
        'slack_avatar_path'
    )

    list_per_page = 60

    def get_avatar_as_thumbnail(self, obj):
        if obj.slack_avatar_path:
            return mark_safe('<img class="img-responsive" src="{avatar_path}" width="100" height="100" />'.format(
                avatar_path=obj.slack_avatar_path
            ))

        return 'No avatar found'

    get_avatar_as_thumbnail.allow_tags = True
    get_avatar_as_thumbnail.short_description = 'User\'s avatar'
