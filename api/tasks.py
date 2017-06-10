# -*- coding: utf-8 -*-

import os
from io import BytesIO

import requests
from celery import shared_task
from django.db import IntegrityError

from api.models import SlackConfiguration
from api.models import SlackUsers, SlackChannels, SlackMessages, SlackFiles, SlackPrivateChannels, SlackTeamEmojis
from api.utils import get_channel_messages, get_all_users_data, get_all_users_files, get_all_team_emoji, StreamFile
from api.utils import get_slack_connection, get_all_channels_data, get_timestamp, get_private_channels_data

try:
    from requests.packages.urllib3.contrib import pyopenssl

    pyopenssl.inject_into_urllib3()
except ImportError:
    pass


@shared_task(
    name='get_slack_users_task',
    queue='slack_update_db'
)
def get_slack_users_task():
    """
    Celery task to update SlackUsers model.
    """

    try:
        sc = get_slack_connection()

        slack_users = get_all_users_data(sc)

        for slack_user in slack_users:
            try:
                SlackUsers.objects.get_or_create(
                    slack_id=slack_user[0],
                    slack_username=slack_user[1],
                    slack_email=slack_user[2],
                    slack_avatar_path=slack_user[3]
                )
            except IntegrityError:
                pass
    except:
        pass


@shared_task(
    name='get_slack_channels_task',
    queue='slack_update_db'
)
def get_slack_channels_task():
    """
    Celery task to update SlackChannels model.
    """

    try:
        sc = get_slack_connection()

        slack_channels = get_all_channels_data(sc)

        for slack_channel in slack_channels:
            channel_members = SlackUsers.objects.filter(
                slack_id__in=slack_channel[2]
            ).values_list('slack_username', flat=True)

            members = ', '.join([m for m in channel_members if m])

            try:
                SlackChannels.objects.get_or_create(
                    channel_name=slack_channel[0],
                    channel_id=slack_channel[1],
                    members=members,
                    number_of_members=slack_channel[3],
                    channel_description=slack_channel[4],
                )

            except IntegrityError:
                pass
    except:
        pass


@shared_task(
    name='get_slack_private_channels_task',
    queue='slack_update_db'
)
def get_slack_private_channels_task():
    """
    Celery task to update SlackPrivateChannels model.
    """

    try:
        sc = get_slack_connection()

        slack_private_channels = get_private_channels_data(sc)

        for slack_priv_channel in slack_private_channels:
            channel_members = SlackUsers.objects.filter(
                slack_id__in=slack_priv_channel[3]
            ).values_list('slack_username', flat=True)

            channel_creator = SlackUsers.objects.filter(
                slack_id=slack_priv_channel[2]
            ).values_list('slack_username', flat=True)

            private_channel_creator = ''.join(channel_creator)
            private_channel_members = ', '.join([m for m in channel_members if m])

            try:
                SlackPrivateChannels.objects.get_or_create(
                    private_channel_name=slack_priv_channel[0],
                    private_channel_id=slack_priv_channel[1],
                    private_channel_creator=private_channel_creator,
                    private_channel_members=private_channel_members,
                    private_channel_value=slack_priv_channel[4],
                    private_channel_topic=slack_priv_channel[5],
                )

            except IntegrityError:
                pass
    except:
        pass


@shared_task(
    name='get_posted_by_users_files_task',
    queue='slack_update_db',
)
def get_posted_by_users_files_task():
    """
    Celery task to retrieve files posted by users.
    """

    try:
        sc = get_slack_connection()

        slack_files = get_all_users_files(sc)

        for slack_file in slack_files:
            username = SlackUsers.objects.filter(
                slack_id=slack_file[0]
            ).values_list('slack_username', flat=True)

            if not ''.join(username):
                username = SlackUsers.objects.filter(
                    slack_id=slack_file[0]
                ).values_list('slack_email', flat=True)

            timestamp = get_timestamp(slack_file[2])

            user = ''.join(username)

            try:
                SlackFiles.objects.get_or_create(
                    user=user,
                    file_path=slack_file[1],
                    timestamp=timestamp
                )

            except IntegrityError:
                pass
    except:
        pass


@shared_task(
    name='download_posted_by_users_files_task',
    queue='slack_download_posted_files',
)
def download_posted_by_users_files_task():
    """
    Celery task to download posted by users files and store them as FileField objects.
    """

    from api.models import SlackFiles

    posted_files = SlackFiles.objects.filter(download_status=False)

    for posted_file in posted_files:
        download_single_posted_by_user_file_task.delay(posted_file.id)

#TODO: Not working right now.
@shared_task(
    name='download_single_posted_by_user_file_task',
    queue='slack_download_posted_files',
)
def download_single_posted_by_user_file_task(file_pk):
    """
    Celery task to download single file posted by Slack user. 
    """

    from api.models import SlackFiles

    file_item = SlackFiles.objects.get(pk=file_pk)

    file_url = file_item.file_path
    file_name = os.path.basename(file_url)

    api_token = SlackConfiguration.get_solo().api_token

    payload = {
        'email': 'x',
        'password': 'x',
        'token': api_token
    }

    with requests.session() as session:
        session.post(file_url, params=payload)
        session.headers.update(dict(referer=file_url))

        r = session.get(
            file_url,
            stream=True
        )

        file_content = r.content

        buffer = BytesIO(file_content)
        django_file = StreamFile(buffer)

        file_item.user_file.save(
            file_name,
            django_file,
            save=True
        )

        file_item.download_status = True
        file_item.save()


@shared_task(
    name='get_channel_messages_task',
    queue='slack_update_db',
)
def get_channel_messages_task():
    """
    Celery task to retrieve messages for channels.
    """

    try:
        sc = get_slack_connection()
        slack_channels = get_all_channels_data(sc)

        slack_channels_ids = [channel_id[1] for channel_id in slack_channels]

        for channel_id in slack_channels_ids:
            author__message_data = get_channel_messages(sc, channel_id)

            for author_and_message in author__message_data:
                name = SlackChannels.objects.filter(
                    channel_id=channel_id
                ).values_list('channel_name', flat=True)

                author = SlackUsers.objects.filter(
                    slack_id=author_and_message[0]
                ).values_list('slack_username', flat=True)

                channel_name = ''.join(name)
                username = ''.join(author)
                timestamp = get_timestamp(author_and_message[2])

                try:
                    SlackMessages.objects.get_or_create(
                        channel_name=channel_name,
                        message=author_and_message[1],
                        author_of_message=username,
                        timestamp=timestamp,
                    )
                except IntegrityError:
                    pass
    except:
        pass


@shared_task(
    name='get_team_emojis_task',
    queue='slack_update_db',
)
def get_team_emojis_task():
    """
    Celery task to get all team's emojis.
    """

    try:
        sc = get_slack_connection()

        emojis = get_all_team_emoji(sc)

        for emoji_item in emojis:
            try:
                SlackTeamEmojis.objects.get_or_create(
                    emoji=emoji_item[0],
                    emoji_path=emoji_item[1],
                )
            except IntegrityError:
                pass
    except:
        pass
