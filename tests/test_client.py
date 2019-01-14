import inspect
from datetime import datetime, timedelta
import os, pytest

from ..insight import application
from googleapiclient.http import HttpMock


class TestBase:
    cals_mock = None
    events_mock = None
    credentials_mock = None
    request_builder_mock = None
    authentication_mock = None
    response_mock = HttpMock(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +
                             '/resources/calendar_list_resp.json', headers={'status': '200'})

    first_date = datetime(2018, 11, 19).astimezone()
    second_date = (datetime(2018, 11, 20).astimezone() + timedelta(1))

    @pytest.fixture(autouse=True)
    def client(self, mocker):
        self.cals_mock = mocker.patch('app.services.calendar_service.get_calendars')
        self.events_mock = mocker.patch('app.services.events_service.get_events')
        self.credentials_mock = mocker.patch('app.services.authentication_service.get_credentials')
        self.authentication_mock = mocker.patch('app.services.authentication_service.create_auth_request')

        self.cals_mock.return_value = [dict(id='testId', etag='"testEtag"', primary=True, summary='test@test.com',
                                            colorId='1'),
                                       dict(id='testId2', etag='"wrong"', primary=False, summary='test1@test.com',
                                            colorId='2')]
        self.events_mock.return_value = [dict(start=dict(dateTime=self.first_date.isoformat()),
                                              end=dict(dateTime=self.second_date.isoformat()),
                                              summary="test")]
        self.credentials_mock.return_value = self.response_mock
        self.authentication_mock.return_value = None

        application.config['TESTING'] = True
        yield application.test_client()
