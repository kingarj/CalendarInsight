from ..utilities.util import suffix, convert_date, format_date
from .test_client import TestBase

from datetime import datetime, timezone


class TestUtilities(TestBase):

    def test_suffix(self):
        firsts = [1, 21, 201, 42342341]
        seconds = [2, 22, 102, 14342]
        thirds = [3, 23, 303, 32432423]
        others = range(4, 20)
        for i in firsts:
            assert suffix(i) == 'st'
        for i in seconds:
            assert suffix(i) == 'nd'
        for i in thirds:
            assert suffix(i) == 'rd'
        for i in others:
            assert suffix(i) == 'th'

    def test_date_conversion(self):
        one = "2018-10-01T12:00:00.00000+00:00"
        two = "2018-10-01T12:00:00.00000+01:00"
        three = "2018-10-01T12:00:00.00000+12:00"
        four = "2018-10-01T12:00:00.00000"
        five = "2018-10-01T12:00:00000"
        six = {
            'date': '2018-10-01'
        }
        seven = {
            'dateTime': self.first_date.isoformat()
        }
        # we won't accept dates that do not include seconds
        eight = "2018-10-01T12:00"
        dates = [self.first_date.isoformat(), self.second_date.isoformat(), one, two, three, four, five, six, seven]

        # assertions
        for date in dates:
            assert type(convert_date(date)) is datetime
        try:
            convert_date(eight)
        except ValueError:
            # we would not expect this date to be converted
            assert True

    def test_date_formatting(self):
        date = datetime.now(timezone.utc).astimezone()
        formatted = format_date(date)
        assert len(formatted) == 4
        assert type(formatted['day']) == str
        assert type(formatted['month']) == str
        assert formatted['year'] == date.year
        assert type(formatted['year']) == int
        assert type(formatted['date']) == str
