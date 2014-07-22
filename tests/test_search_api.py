from search import server

import unittest
import json
import calendar
import mock


class SearchAPITestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()


    @mock.patch("search.es.Search.get")
    def test_search(self, mock_get):
        title_number = 'DN100'
        mock_get.return_value = {'title_number' : title_number }

        rv = self.app.get('/search?query=' + title_number)
        mock_get.assert_called_with(u'dn100')

        assert 'DN100' in rv.data

    @mock.patch("search.es.Search.search")
    def test_get_one_title_back(self, mock_search):
        title_number = 'DN100'

        rv = self.app.get('/titles/' + title_number)
        mock_search.assert_called_with(
            index='public_titles',
            body={
                'query': {
                    'match': {
                        'title_number': title_number
                    }
                }
            })

    @mock.patch("search.es.Search.index")
    def test_load(self, mock_index):
        index = 'authenticated_titles'
        data = json.dumps({'foo':'bar'})

        # call with "some" json...
        self.app.put('/load/' + index, data=data, content_type='application/json')
        mock_index.assert_called_with(
            index=index, doc_type="titles", body=json.loads(data)
        )
