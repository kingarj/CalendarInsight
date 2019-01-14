import os.path
from .test_client import TestBase


class TestRoutes(TestBase):

    def test_get_index(self, client):
        """
        Tests that a successful GET request can be made to the index page.
        """
        resp = client.get('/')
        assert resp.status_code == 200

    def test_post_index_no_matching_query(self, client):
        """
        Tests that you are returned a success code even if your query doesn't match any event summaries of a given
        calendar.
        """
        resp = client.post('/', data={'query': 'no match', 'calendar': 'test_cal', 'sort_by': 'earliest'})
        assert resp.status_code == 200

    def test_post_index_matching_query(self, client):
        """
        Tests that you can find an event if it matches one of the summaries of a given calendars.
        """
        self.events_mock.return_value = [
            {'summary': 'match',
             'start':
                 {'dateTime': self.first_date.isoformat()},
             'end':
                 {'dateTime': self.second_date.isoformat()}
             }
        ]
        resp = client.post('/', data={'query': 'match', 'calendar': 'test_cal', 'sort_by': 'earliest'})
        assert resp.status_code == 200

    def test_get_analysis(self, client):
        """
        Tests that a successful GET request can be made to the analysis page.
        :param client:
        :return:
        """
        resp = client.get('/analysis')
        assert resp.status_code == 200

    def test_post_analysis(self, client):
        """
        Tests that a successful POST request can be made to the analysis page.
        :param client:
        :return:
        """
        resp = client.post('/analysis', json={'el_id': '2', 'date_val': self.first_date.isoformat(),
                                              'other_date': 'Wednesday November 14th 2018'})
        assert resp.status_code == 200
        assert os.path.isfile('src/' + resp.json['fileName'])
