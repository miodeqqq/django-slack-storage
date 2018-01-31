# -*- coding: utf-8 -*-

import os
from api.utils import convert_size
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

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackTeamEmojisAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions


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

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackPrivateChannelsAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions


@admin.register(SlackFiles)
class SlackFilesAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'user_file',
        'file_size',
        'file_content_type',
        'file_sha256_checksum',
        'file_path',
        'download_status',
        'timestamp'
    )

    list_display = (
        'user',
        'get_user_file',
        'get_filesize',
        'download_status',
        'get_file_path_as_url',
        'timestamp'
    )

    list_filter = (
        'user',
        'download_status',
        'file_content_type'
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
        'file_size',
        'timestamp',
        'file_content_type',
        'file_sha256_checksum'
    )

    list_per_page = 60

    def get_filesize(self, obj):
        """
        Returns human readable filesize for downloaded files.
        """

        return convert_size(obj.file_size)

    get_filesize.allow_tags = True
    get_filesize.admin_order_field = 'file_size'
    get_filesize.short_description = 'File size'

    def get_user_file(self, obj):
        if obj.user_file:
            file_url = obj.user_file.url
            file_url = file_url.split('media')[-1]

            return '<a href="/media{file_path}" target="_blank">{file_name}</a>'.format(
                file_path=file_url,
                file_name=os.path.basename(obj.user_file.path)
            )
        else:
            return '<span style="color:red">Not yet...</span>'

    get_user_file.allow_tags = True
    get_user_file.admin_order_field = 'user_file'
    get_user_file.short_description = 'Downloaded file'

    def get_file_path_as_url(self, obj):
        if obj.file_path:
            return format_html('<a href="{file_path}" target="_blank">{file_path}</a>'.format(
                file_path=obj.file_path
            ))

        return 'No URL.'

    get_file_path_as_url.allow_tags = True
    get_file_path_as_url.short_description = 'File URL'

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackFilesAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions


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

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackChannelsAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions


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

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackMessagesAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions


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

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Employee'):
            return False

        return True

    def get_actions(self, request):
        actions = super(SlackUsersAdmin, self).get_actions(request)

        if request.user.groups.filter(name='Employee'):
            del actions['delete_selected']

        return actions
