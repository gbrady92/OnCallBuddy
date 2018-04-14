from authorise import get_credentials

SLACK = get_credentials()


def get_user_by_email(email):
    return SLACK.api_call("users.lookupByEmail", email=email)


def private_message_user(user_id, message_text=None):
    private_message_obj = SLACK.api_call("im.open", user=user_id)

    private_channel_id = private_message_obj['channel']['id']

    return SLACK.api_call(
        "chat.postMessage", channel=private_channel_id, text=message_text)
