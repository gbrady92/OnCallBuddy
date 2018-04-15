from datetime import datetime, timedelta
import calendar
import json

from google_cal import api
from slack import api as slack_api

CALENDAR_IDS = api.get_calendar_ids()


def get_first_last_day_of_current_month(current_date):
    current_date = datetime.combine(current_date, datetime.min.time())
    first_day = current_date.replace(
        day=1
    )

    last_day = first_day.replace(
        day=calendar.monthrange(first_day.year, first_day.month)[1])
    last_day = datetime.combine(last_day, datetime.max.time())

    return first_day, last_day


def parse_and_store_event(rota, event):
    rota.setdefault(event['summary'].split('-')[1].strip(), []).append([
        datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ'),
        datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
    ])


def get_engineers_on_call():
    rota = {}
    start, end = get_first_last_day_of_current_month(datetime.now())

    primary_oncall_events = api.get_events_for_calendar_id(
        CALENDAR_IDS['primary'], start, end)
    secondary_oncall_events = api.get_events_for_calendar_id(
        CALENDAR_IDS['secondary'], start, end)

    for event in primary_oncall_events:
        parse_and_store_event(rota, event)

    for event in secondary_oncall_events:
        parse_and_store_event(rota, event)

    return rota


def run_on_call_bot():
    oncall_rota = get_engineers_on_call()
    # on_call_engineer_names = oncall_rota.keys()
    on_call_engineer_names = ['Gareth Brady']
    on_call_engineer_slack_ids = {
        name: slack_api.get_slack_user_by_name(name)
        for name in on_call_engineer_names
    }

    for name, slack_id in on_call_engineer_slack_ids.iteritems():
        message = 'Hi, You are on call these dates this month: \n'
        for date_range in oncall_rota[name]:
            message += "{} - {} \n".format(
                date_range[0].strftime("%d-%m-%Y"),
                date_range[1].strftime("%d-%m-%Y"))
        slack_api.private_message_user(slack_id, message)
