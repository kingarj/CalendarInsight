from . import util, authentication_service, cache, application


@cache.memoize()
def get_events(calendar, time_max=None, time_min=None):
    """
    Method to retrieve a list of events from the Google Calendar API.
    :param calendar: the identifier of the calendar
    :param time_max: optional start time (upper bound for event retrieval)
    :param time_min: optional end time (lower bound for event retrieval)
    :return: a list of events
    """
    service = authentication_service.get_service()

    events_result = service.events().list(calendarId=calendar, orderBy='startTime', singleEvents=True, timeMin=time_min,
                                          timeMax=time_max).execute()
    application.logger.debug('API call - events list')
    events = events_result.get('items', [])

    return events


def get_duration(event):
    """
    Given an event, calculate its duration
    :param event
    :return: a timedelta, such that days, hours, minutes or seconds can be derived
    """
    end = util.convert_date(event['end'])
    start = util.convert_date(event['start'])
    return end - start


def calculate_days_hours_minutes(event):
    """
    Given an event, calculate the days, hours and minutes that it lasts
    :param event
    :return: the duration in days, hours and minutes
    """
    try:
        duration = get_duration(event)
        days = duration.days
        hours = duration.seconds // 3600
        minutes = duration.seconds // 60 % 60
        return days, hours, minutes
    except TypeError as e:
        application.logger.error(e)
    return 0, 0, 0


def search(cal_id, query, sort):
    """
    Filter a list of events to find matches to a given query.
    :param cal_id: the identifier of the calendar
    :param query: either a word, phrase or the empty string
    :param sort: ascending ('earliest') or descending ('latest')
    :return: a list of events matching the query, as well as the total number of days, hours and minutes spent in all
    of those events
    """
    events = get_events(cal_id)
    matches = []
    days = 0
    hours = 0
    minutes = 0
    for ev in events:
        if query.lower() in ev['summary'].lower():
            if 'dateTime' in ev['start'] and 'dateTime' in ev['end']:
                duration = calculate_days_hours_minutes(ev)
                days += duration[0]
                hours += duration[1]
                minutes += duration[2]
            ev = format_event(ev)
            if sort == 'earliest':
                matches.append(ev)
            elif sort == 'latest':
                matches.insert(0, ev)

    hours += minutes // 60
    minutes -= (minutes // 60) * 60
    days += hours // 24
    hours -= (hours // 24) * 24

    return matches, days, hours, minutes


def format_event(event):
    """
    Convert the event object into one that can be more easily used by the template to display results
    :param event
    :return: a dict with the required attributes correctly formatted
    """
    start = util.convert_date(event['start'])
    end = util.convert_date(event['end'])
    start_time = start.strftime("%H:%M") if start.hour != 0 else None
    end_time = end.strftime("%H:%M") if end.hour != 0 else None

    formatted = {'summary': event['summary'],
                 'location': event['location'] if 'location' in event else None,
                 'description': event['description'] if 'description' in event else None,
                 'start_day_num': start.day,
                 'start_day_text': start.strftime("%A"),
                 'end_day_text': end.strftime("%A") if not end_time else None,
                 'start_month': start.strftime("%B"),
                 'start_time': start_time,
                 'end_time': end_time}

    return formatted
