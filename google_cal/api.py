from datetime import datetime
import pytz


from authorise import get_credentials
import const

import googleapiclient.discovery


def create_calendar_object():
    credentials = get_credentials()
    return googleapiclient.discovery.build(
        const.API_SERVICE_NAME, const.API_VERSION, credentials=credentials)


def get_calendar_ids():
    result = {}
    calendar = create_calendar_object()

    calendar_list = calendar.calendarList().list().execute()

    for cal in calendar_list['items']:
        if cal['summary'] == "On Call Schedule for Primary On-Call":
            result['primary'] = cal['id']
        if cal['summary'] == "On Call Schedule for Secondary On Call":
            result['secondary'] = cal['id']
        if cal['summary'] == "Product/Engineering Holidays":
            result['holiday'] = cal['id']

    return result


def get_events_for_calendar_id(calendar_id, start, end):
    calendar = create_calendar_object()

    start = pytz.UTC.localize(start).isoformat()
    end = pytz.UTC.localize(end).isoformat()

    event_list = calendar.events().list(
        calendarId=calendar_id, timeMin=start, timeMax=end).execute()

    return event_list['items']

