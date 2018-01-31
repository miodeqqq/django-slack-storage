# -*- coding: utf-8 -*-

import hashlib
import logging
import os
from io import BytesIO

from celery import shared_task
from magic import from_buffer
from requests import get

from api.models import SlackConfiguration
from api.models import SlackUsers, SlackChannels, SlackMessages, SlackFiles, SlackPrivateChannels, SlackTeamEmojis
from api.utils import get_channel_messages, get_all_users_data, get_all_users_files, get_all_team_emoji, StreamFile
from api.utils import get_slack_connection, get_all_channels_data, get_timestamp, get_private_channels_data

logger = logging.getLogger(__name__)


@shared_task(
    name='get_slack_users_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_slack_users_task(self):
    """
    Celery task to update SlackUsers model.
    """

    try:
        sc = get_slack_connection()

        slack_users = get_all_users_data(sc)

        for slack_user in slack_users:
            if not SlackUsers.objects.filter(slack_id=slack_user[0]).exists():
                SlackUsers.objects.create(
                    slack_id=slack_user[0],
                    slack_username=slack_user[1],
                    slack_email=slack_user[2],
                    slack_avatar_path=slack_user[3]
                )

    except Exception as exc:
        logger.info('[get_slack_users_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='get_slack_channels_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_slack_channels_task(self):
    """
    Celery task to update SlackChannels model.
    """

    try:
        sc = get_slack_connection()

        slack_channels = get_all_channels_data(sc)

        for slack_channel in slack_channels:
            if not SlackChannels.objects.filter(channel_id=slack_channel[1]).exists():
                channel_members = SlackUsers.objects.filter(
                    slack_id__in=slack_channel[2]
                ).values_list('slack_username', flat=True)

                members = ', '.join([m for m in channel_members if m])

                SlackChannels.objects.create(
                    channel_name=slack_channel[0],
                    channel_id=slack_channel[1],
                    members=members,
                    number_of_members=slack_channel[3],
                    channel_description=slack_channel[4],
                )

    except Exception as exc:
        logger.info('[get_slack_channels_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='get_slack_private_channels_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_slack_private_channels_task(self):
    """
    Celery task to update SlackPrivateChannels model.
    """

    try:
        sc = get_slack_connection()

        slack_private_channels = get_private_channels_data(sc)

        for slack_priv_channel in slack_private_channels:
            if not SlackPrivateChannels.objects.filter(private_channel_id=slack_priv_channel[1]).exists():
                channel_members = SlackUsers.objects.filter(
                    slack_id__in=slack_priv_channel[3]
                ).values_list('slack_username', flat=True)

                channel_creator = SlackUsers.objects.filter(
                    slack_id=slack_priv_channel[2]
                ).values_list('slack_username', flat=True)

                private_channel_creator = ''.join(channel_creator)
                private_channel_members = ', '.join([m for m in channel_members if m])

                SlackPrivateChannels.objects.create(
                    private_channel_name=slack_priv_channel[0],
                    private_channel_id=slack_priv_channel[1],
                    private_channel_creator=private_channel_creator,
                    private_channel_members=private_channel_members,
                    private_channel_value=slack_priv_channel[4],
                    private_channel_topic=slack_priv_channel[5],
                )

    except Exception as exc:
        logger.info('[get_slack_private_channels_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='get_posted_by_users_files_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_posted_by_users_files_task(self):
    """
    Celery task to retrieve files posted by users.
    """

    try:
        sc = get_slack_connection()

        slack_files = get_all_users_files(sc)

        users_in_db = SlackUsers.objects.values_list('pk', flat=True)

        if users_in_db:
            for slack_file in slack_files:
                slack_user = SlackUsers.objects.filter(slack_id=slack_file[0])

                if slack_user.exists():
                    user = slack_user.first().slack_email

                    if not SlackFiles.objects.filter(file_path=slack_file[1]).exists():
                        SlackFiles.objects.create(
                            user=user,
                            file_path=slack_file[1],
                            timestamp=get_timestamp(slack_file[2])
                        )

    except Exception as exc:
        logger.info('[get_posted_by_users_files_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='download_posted_by_users_files_task',
    queue='slack_download_posted_files',
)
def download_posted_by_users_files_task():
    """
    Celery task to download posted by users files and store them as FileField objects.
    """

    from api.models import SlackFiles

    posted_files = SlackFiles.objects.filter(download_status=False).values_list('pk', flat=True)

    for posted_file_id in posted_files:
        download_single_posted_by_user_file_task.delay(posted_file_id)


@shared_task(
    name='download_single_posted_by_user_file_task',
    queue='slack_download_posted_files',
    max_retries=10,
    bind=True
)
def download_single_posted_by_user_file_task(self, file_pk):
    """
    Celery task to download single file posted by Slack user. 
    """

    from api.models import SlackFiles

    try:
        file_item = SlackFiles.objects.get(pk=file_pk)

        file_url = file_item.file_path
        file_name = os.path.basename(file_url)[:255]

        api_token = SlackConfiguration.get_solo().api_token

        headers = {
            'Authorization': 'Bearer ' + api_token
        }

        r = get(
            file_url,
            stream=True,
            headers=headers
        )

        file_content = r.content

        file_sha256_checksum = hashlib.sha256(file_content).hexdigest()
        file_content_type = from_buffer(file_content)[:255]

        file_sha256_exists = SlackFiles.objects.filter(
            file_sha256_checksum=file_sha256_checksum
        ).exists()

        if not file_sha256_exists:
            buffer = BytesIO(file_content)
            django_file = StreamFile(buffer)

            file_item.user_file.save(
                file_name,
                django_file,
                save=True
            )

            file_item.file_content_type = file_content_type
            file_item.file_sha256_checksum = file_sha256_checksum
            file_item.download_status = True

            file_item.save()

            if os.path.exists(file_item.user_file.path):
                file_item.file_size = os.stat(file_item.user_file.path).st_size
                file_item.save()

    except Exception as exc:
        logger.info('[download_single_posted_by_user_file_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='get_channel_messages_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_channel_messages_task(self):
    """
    Celery task to retrieve messages for channels.
    """

    try:
        # check if channel ids are in db
        slack_channels_ids = SlackChannels.objects.values_list('channel_id', flat=True)

        if slack_channels_ids:
            slack_users = SlackUsers.objects.values_list('slack_id', flat=True)

            if slack_users:
                sc = get_slack_connection()

                for channel_id in slack_channels_ids:
                    author__message_data = get_channel_messages(sc, channel_id)

                    if author__message_data is not None:
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

                            if not SlackMessages.objects.filter(channel_name=channel_name, message=author_and_message[1]).exists():
                                SlackMessages.objects.create(
                                    channel_name=channel_name,
                                    message=author_and_message[1],
                                    author_of_message=username,
                                    timestamp=timestamp,
                                )

    except Exception as exc:
        logger.info('[get_channel_messages_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)


@shared_task(
    name='get_team_emojis_task',
    queue='slack_update_db',
    max_retries=10,
    bind=True
)
def get_team_emojis_task(self):
    """
    Celery task to get all team's emojis.
    """

    try:
        sc = get_slack_connection()

        emojis = get_all_team_emoji(sc)

        for emoji_item in emojis:
            if not SlackTeamEmojis.objects.filter(emoji=emoji_item[0]).exists():
                SlackTeamEmojis.objects.create(
                    emoji=emoji_item[0],
                    emoji_path=emoji_item[1],
                )


    except Exception as exc:
        logger.info('[get_team_emojis_task] Error --> {exc}'.format(exc=exc))
        self.retry(exc=exc)
