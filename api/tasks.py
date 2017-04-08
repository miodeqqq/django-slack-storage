# -*- coding: utf-8 -*-

from celery import shared_task
from django.db import IntegrityError

from api.models import SlackUsers, SlackChannels, SlackMessages, SlackFiles
from api.utils import get_channel_messages, get_all_users_data, get_all_users_files
from api.utils import get_slack_connection, get_all_channels_data, get_timestamp


@shared_task(
    name='get_slack_users_task',
    queue='slack_update_db'
)
def get_slack_users_task():
    """
    Celery task to update SlackUsers model.
    """

    sc = get_slack_connection()

    slack_users = get_all_users_data(sc)

    for slack_user in slack_users:
        SlackUsers.objects.get_or_create(
            slack_id=slack_user[0],
            slack_username=slack_user[1],
            slack_email=slack_user[2],
            slack_avatar_path=slack_user[3]
        )

@shared_task(
    name='get_slack_channels_task',
    queue='slack_update_db'
)
def get_slack_channels_task():
    """
    Celery task to update SlackChannels model.
    """

    sc = get_slack_connection()

    slack_channels = get_all_channels_data(sc)

    for slack_channel in slack_channels:
        try:
            SlackChannels.objects.update_or_create(
                channel_name=slack_channel[0],
                channel_id=slack_channel[1],
                members=', '.join([m for m in slack_channel[2] if m]),
                number_of_members=slack_channel[3],
                channel_description=slack_channel[4],
            )

        except IntegrityError:
            pass

@shared_task(
    name='get_posted_by_users_files_task',
    queue='slack_update_db',
)
def get_posted_by_users_files_task():
    """
    Celery task to retrieve files posted by users.
    """

    sc = get_slack_connection()

    slack_files = get_all_users_files(sc)

    for slack_file in slack_files:

        timestamp = get_timestamp(slack_file[2])

        SlackFiles.objects.get_or_create(
            user=slack_file[0],
            file_path=slack_file[1],
            timestamp=timestamp
        )


@shared_task(
    name='get_channel_messages_task',
    queue='slack_update_db',
)
def get_channel_messages_task():
    """
    Celery task to retrieve messages for channels.
    """

    sc = get_slack_connection()

    slack_channels = get_all_channels_data(sc)

    slack_channels_ids = [channel_id[1] for channel_id in slack_channels]

    for channel_id in slack_channels_ids:
        author__message_data = get_channel_messages(sc, channel_id)

        for author_and_message in author__message_data:
            channel_name = ''.join(
                SlackChannels.objects.filter(
                    channel_id=channel_id
                ).values_list('channel_name', flat=True)
            )

            username = ''.join(
                SlackUsers.objects.filter(
                    slack_id=author_and_message[0]
                ).values_list('slack_username', flat=True)
            )

            timestamp = get_timestamp(author_and_message[2])

            try:
                SlackMessages.objects.update_or_create(
                    channel_name=channel_name,
                    message=author_and_message[1],
                    author_of_message=username,
                    timestamp=timestamp
                )
            except IntegrityError:
                pass