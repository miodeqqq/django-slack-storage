# -*- coding: utf-8 -*-

import math
from datetime import datetime

from django.core.files.base import ContentFile
from slackclient import SlackClient

from api.models import SlackConfiguration


def convert_size(size_bytes):
    """
    General method to convert bytes into human readable size.
    """

    if size_bytes == 0:
        return '0B'

    size_name = (
        'B',
        'KB',
        'MB',
        'GB'
    )

    i = int(math.floor(math.log(size_bytes, 1024)))

    p = math.pow(1024, i)

    s = round(size_bytes / p, 2)

    return '{filesize} {size_type}'.format(
        filesize=s,
        size_type=size_name[i]
    )


class StreamFile(ContentFile):
    """
    Helpful class for downloaded big files.
    """

    def __init__(self, stream):
        super(ContentFile, self).__init__(stream)
        stream.seek(0, 2)
        self.size = stream.tell()


def get_slack_connection():
    """
    General method to connect to Slack using API token.
    """

    return SlackClient(SlackConfiguration.get_solo().api_token)


def get_all_channels_data(sc):
    """
    General method to return all channels data.
    """

    channels = sc.api_call("channels.list")

    channels_data = []

    for channel_item in channels.get('channels', None):
        channel_name = channel_item.get('name', None).strip()
        channel_id = channel_item.get('id', None).strip()
        channel_members = channel_item.get('members', None)
        channel_num_members = channel_item.get('num_members', None)
        channel_description = channel_item.get('topic', {}).get('value', None).strip()

        channel__items = channel_name, channel_id, channel_members, channel_num_members, channel_description

        channels_data.append(channel__items)

    final_channel_data = [c for c in channels_data if c]

    return final_channel_data


def get_private_channels_data(sc):
    """
    General method to get all private channels data.
    """

    private_channels = sc.api_call("groups.list")

    priv__channels_data = []

    for priv_item in private_channels.get('groups'):
        channel_name = priv_item.get('name').strip()
        channel_id = priv_item.get('id').strip()
        channel_creator = priv_item.get('creator').strip()
        channel_members = priv_item.get('members')
        channel_purpose_value = priv_item.get('purpose', {}).get('value', '').strip()
        channel_topic = priv_item.get('topic', {}).get('value', '').strip()

        priv_channels__items = channel_name, channel_id, channel_creator, channel_members, channel_purpose_value, channel_topic

        priv__channels_data.append(priv_channels__items)

    final_priv_channel_data = [c for c in priv__channels_data if c]

    return final_priv_channel_data


def get_all_users_data(sc):
    """
    General method to get all slack users.
    """

    users = sc.api_call("users.list")

    team_members_data = []

    slack_members = users.get('members')

    slack_members = [user for user in slack_members if not user.get('deleted')]

    for user in slack_members:
        user_data = user.get('profile').get('real_name')

        if 'slackbot' not in user_data and 'HeyTaco!' not in user_data:
            user_image_other = user.get('profile', {}).get('image_192')
            user_image = user.get('profile', {}).get('image_original', user_image_other)
            user_email = user.get('profile', {}).get('email', '')
            user_name = user.get('profile', {}).get('real_name_normalized')
            user_id = user.get('id')

            single_user__data = user_id, user_name, user_email, user_image

            team_members_data.append(single_user__data)

    users_data = [user for user in team_members_data if user]

    return users_data


def get_channel_messages(sc, channel_id):
    """
    General method to return messages for given channel ID.
    """

    history = sc.api_call("channels.history", channel=channel_id)

    messages = []

    history_msgs = history.get('messages', [])

    if history_msgs:
        for message_item in history_msgs:
            if message_item.get('user') and message_item.get('text'):
                user = message_item.get('user').strip()
                message = message_item.get('text').strip()
                ts = message_item.get('ts')

                user__message_ts = user, message, ts

                messages.append(user__message_ts)

        final_messages = [tuple(filter(None, t)) for t in messages if t[0]]

        return final_messages


def get_all_users_files(sc):
    """
    General method to get all files posted/added by users.
    """

    files = sc.api_call("files.list")

    files__users_data = []

    files_urls = files.get('files', [])

    if files_urls:
        for file_item in files_urls:
            url = file_item.get('url_private_download', [])

            if url:
                username = file_item.get('user', '').strip()
                timestamp = file_item.get('timestamp')

                _user_data = ''.join(username), url, timestamp

                files__users_data.append(_user_data)

    final__users_data = [f for f in files__users_data if f]

    return final__users_data


def get_all_team_emoji(sc):
    """
    General method to get all team's custom emoji.
    """

    emojis = sc.api_call('emoji.list')

    emoji_data = []

    for emoji_item in emojis.get('emoji', {}).items():
        emoji_value = emoji_item[0]
        emoji_url_or_shortcut = emoji_item[1]

        emoji__value = emoji_value, emoji_url_or_shortcut

        emoji_data.append(emoji__value)

    return emoji_data


def get_timestamp(ts):
    """
    General method to convert timestamp into string.
    """

    return str(datetime.utcfromtimestamp(float(ts)))
