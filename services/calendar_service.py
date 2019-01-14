from ..insight import cache, application

from .authentication_service import get_service


@cache.memoize()
def get_calendars():
    """
    Retrieves a list of calendars from the currently authenticated user
    :return: a calendar list
    """
    service = get_service()

    calendar_list = service.calendarList().list().execute()
    application.logger.debug("API call - calendarList list")
    calendars = calendar_list.get('items', [])

    return calendars


def get_primary_etag(calendar_list):
    """
    Given a list of calendars, finds the primary calendar and returns the etag from that calendar object.
    :param calendar_list: a list of calendars from the authenticated user
    :return: an etag
    """
    primary_cals = [cal['etag'] for cal in calendar_list if cal.get('primary')]
    return primary_cals[0][1:-1]
