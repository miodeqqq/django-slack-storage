# -*- coding: utf-8 -*-

from slackclient import SlackClient
from api.models import SlackConfiguration, SlackUsers
from datetime import datetime

def get_slack_connection():
    """
    General method to connect to Slack using API token.
    """

    token = SlackConfiguration.get_solo().api_token

    return SlackClient(token=token)


def get_all_channels_data(sc):
    """
    General method to return all channels data.
    """

    channels = sc.api_call("channels.list")

    channels_data = []

    for channel_item in channels.get('channels', None):
        channel_name = channel_item.get('name', None).strip()
        channel_id = channel_item.get('id', None).strip()

        channel_members = SlackUsers.objects.filter(
            slack_id__in=channel_item.get('members', None)
        ).values_list('slack_username', flat=True)

        channel_num_members = channel_item.get('num_members', None)
        channel_description = channel_item.get('topic', {}).get('value', None).strip()

        channel__items = channel_name, channel_id, channel_members, channel_num_members, channel_description

        channels_data.append(channel__items)

    final_channel_data = [c for c in channels_data if c]

    return final_channel_data


def get_all_users_data(sc):
    """
    General method to get all slack users.
    """

    users = sc.api_call("users.list")

    team_members_data = []

    for user in users['members']:
        if not user['deleted']:
            user_data = user.get('profile', None).get('real_name', None)

            if not 'slackbot' in user_data:
                user_image = user.get('profile', {}).get('image_original', None)
                user_name = user.get('profile', {}).get('real_name_normalized', None)
                user_email = user.get('profile', {}).get('email', None)
                user_id = user.get('id', None)

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

    for message_item in history['messages']:
        if message_item.get('user') and message_item.get('text'):
            user__message_ts = message_item.get('user').strip(), message_item.get('text').strip(), message_item.get('ts')
            messages.append(user__message_ts)

    final_messages = [tuple(filter(None, t)) for t in messages if t[0]]

    return final_messages


def get_all_users_files(sc):
    """
    General method to get all files posted/added by users.
    """

    files = sc.api_call("files.list")

    files__users_data = []

    for file_item in files.get('files', None):
        if file_item.get('url_private_download'):
            username = SlackUsers.objects.filter(
                slack_id=file_item.get('user', '').strip()
            ).values_list('slack_username', flat=True)

            user_file = file_item.get('url_private_download')

            timestamp = file_item.get('timestamp')

            _user_data = ''.join(username), user_file, timestamp

            files__users_data.append(_user_data)

    final__users_data = [f for f in files__users_data if f]

    return final__users_data


def get_timestamp(ts):
    """
    General method to convert timestamp into string.
    """

    return str(datetime.utcfromtimestamp(float(ts)))