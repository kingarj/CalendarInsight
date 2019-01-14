from datetime import datetime

from . import events_service
from . import calendar_service
from ..insight import application
import matplotlib
# specify custom backend for matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def get_chart_data(time_max, time_min):
    """
    For each calendar of the authenticated user, this function calculates the total number of minutes spent in events
    for that calendar between time_max and time_min.
    :param time_max: optional start time (upper bound for event retrieval)
    :param time_min: optional end time (lower bound for event retrieval)
    :return: an array of integers representing the number of minutes spent on events in that time period, an array of
    calendar names and an array of calendar colours
    """
    calendars = calendar_service.get_calendars()
    application.logger.debug("API call - calendarList list")
    minutes = []
    names = []
    colours = []

    for cal in calendars:
        events = events_service.get_events(cal['id'], time_max, time_min)
        if len(events) > 0:
            total_minutes = 0
            for ev in events:
                # sum minutes of events for a calendar in a given time period
                try:
                    duration_delta = events_service.get_duration(ev)
                    if duration_delta.seconds > 0:
                        total_minutes += duration_delta.seconds // 60
                    if duration_delta.days > 0:
                        total_minutes += duration_delta.days * 24 * 60
                except TypeError as e:
                    application.logger.error(e)
            if total_minutes > 0:
                names.append(cal['summary'])
                colours.append(cal['colorId'])
                minutes.append(total_minutes)

    return minutes, names, colours


def draw_chart(time_max, time_min, plot_name):
    """
    Uses calendar data to create a pie chart and then save it to a given file path
    :param time_max: optional start time (upper bound for event retrieval)
    :param time_min: optional end time (lower bound for event retrieval)
    :param plot_name: a file path (including name and extension) to save the file to
    """
    hours, names, colours = get_chart_data(time_max, time_min)
    fig1, ax1 = plt.subplots(figsize=(11, 4), subplot_kw=dict(aspect="equal"))
    ax1.pie(hours, autopct='%1.1f%%', startangle=90, pctdistance=1.15)
    ax1.axis('equal')
    ax1.legend(names,
               loc="center left",
               bbox_to_anchor=(0.75, 0, 0.5, 1))
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)
    plt.savefig(plot_name)


def build_file_name(first_date, second_date):
    """
    Helper function to build a file name from primary cal etag and dates of the chart
    :param first_date: one unique identifier
    :param second_date: another unique identifier
    :return: a string for which to name the file
    """
    calendar_list = calendar_service.get_calendars()
    primary_etag = calendar_service.get_primary_etag(calendar_list)
    first = first_date.strftime('%Y-%m-%d')
    second = second_date.strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d-%H')

    return "src/static/plots/" + primary_etag + first + second + now + ".png"
