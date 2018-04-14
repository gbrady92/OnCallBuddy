import json

from slackclient import SlackClient

from const import CREDENTIALS_FILE


def get_credentials():
    bot_token = json.load(open(CREDENTIALS_FILE))['bot_token']
    return SlackClient(bot_token)
