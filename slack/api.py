from authorise import get_credentials

SLACK = get_credentials()


def get_slack_user_by_name(name):
    name = name.lower()
    first, last = name.split(' ')

    # Try first@ Email format
    email = '{}@example.com'.format(first)
    response = SLACK.api_call(
            "users.lookupByEmail", email=email)

    # Try first.last@ format
    if not response['ok']:
        email = '{}.{}@example.com'.format(first, last)
        response = SLACK.api_call(
            "users.lookupByEmail", email=email)

    return response['user']['id']


def private_message_user(user_id, message_text=None):
    private_message_obj = SLACK.api_call("im.open", user=user_id)

    private_channel_id = private_message_obj['channel']['id']

    return SLACK.api_call(
        "chat.postMessage", channel=private_channel_id, text=message_text)
