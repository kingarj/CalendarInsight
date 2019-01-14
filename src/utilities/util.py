from datetime import datetime
from src.insight import application


def format_date(iso):
    day_txt = iso.strftime('%A')
    month_day = iso.strftime('%B {S}').replace('{S}', str(iso.day) + suffix(iso.day))
    datestr = iso.strftime('%d/%m/%Y')
    return dict(day=day_txt, month=month_day, year=iso.year, date=datestr)


def suffix(d):
    """
    Given any number, return its date suffix.
    :param d: a natural number e.g. 1, 30
    :return: a suffix; 'st', 'nd', 'rd' or 'th'
    """
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def convert_date(raw_date):
    """
    Given a date in any potential String format, attempt to return it as a DateTime object
    :param raw_date: String
    :return: a DateTime object if the string can be converted
    """
    timezones = {
        '+00:00': '',
        '+01:00': '+0100',
        '+02:00': '+0200',
        '+03:00': '+0300',
        '+04:00': '+0400',
        '+05:00': '+0500',
        '+06:00': '+0600',
        '+07:00': '+0700',
        '+08:00': '+0800',
        '+09:00': '+0900',
        '+10:00': '+1000',
        '+11:00': '+1100',
        '+12:00': '+1200',
    }
    if 'date' in raw_date:
        return datetime.strptime(raw_date['date'], "%Y-%m-%d")

    elif 'dateTime' in raw_date:
        raw_date = raw_date['dateTime']

    for tz in timezones:
        if tz in raw_date:
            raw_date = raw_date.replace(tz, timezones[tz])

    new_date = raw_date[:-1] if raw_date[-1] == 'Z' else raw_date
    try:
        new_date = datetime.strptime(new_date, "%Y-%m-%dT%H:%M:%S%f%z")
    except ValueError:
        try:
            new_date = datetime.strptime(new_date, "%Y-%m-%dT%H:%M:%S%f")
        except ValueError:
            try:
                new_date = datetime.strptime(new_date, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    new_date = datetime.strptime(new_date, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError as err4:
                    application.logger.warning(err4)
                    raise err4

    return new_date
