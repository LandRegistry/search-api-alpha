from searchapi import server
import unittest
import json
import mock


class SearchAPITestCase(unittest.TestCase):

    test_title_number = 'test0000'

    mock_result = {
        'hits':{
            'hits': [
                {
                '_source': {
                    'title_number': test_title_number,
                    'postcode': ['pl11aa'],
                    'body': {
                        'extent': { },
                        'payment' : {
                            'price_paid': 987654,
                            'titles': [test_title_number]
                        },
                        'previous_sha256': 'cafebabe',
                        'property_description': {
                            'fields': {
                                'addresses': [
                                    {
                                        'house_number': '33',
                                        'postcode': 'PL1 1AA',
                                        'road': 'I hate Road',
                                        'town': 'Town'
                                    }
                                ]
                            },
                            'class_of_title': 'Absolute',
                            'tenure': 'Freehold'
                        },
                        'title_number': test_title_number.upper()
                        }
                    }
                }
                ]
            }
        }

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    @mock.patch('elasticsearch.Elasticsearch.search')
    def test_search(self, mock_es):
        mock_es.return_value = self.mock_result
        rv = self.app.get('/search?query=' + self.test_title_number)
        assert self.test_title_number in rv.data

    @mock.patch('elasticsearch.Elasticsearch.search')
    def test_get_one_public_title_back(self, mock_es):
        mock_es.return_value = self.mock_result
        rv = self.app.get('/titles/' + self.test_title_number)
        mock_es.assert_called_with(
            index='public_titles',
            body={
                'query': {
                    'match': {
                        'title_number': self.test_title_number
                    }
                }
            })

        assert self.test_title_number in rv.data

    @mock.patch('elasticsearch.Elasticsearch.index')
    def test_load(self, mock_index):
        testtn = 'title1'
        index = 'authenticated_titles'
        data = json.dumps({'title_number':testtn, 'foo': 'bar'})

        # call with "some" json...`
        response = self.app.put(
            '/load/' + index,
            data=data,
            content_type='application/json')
        mock_index.assert_called_with(
                index=index,
                id=testtn,
                doc_type="titles",
                body={
                    'title_number': testtn,
                    'postcode': [],
                    'body': json.loads(data)
                    }
        )
        assert response.status == '201 CREATED'

    @mock.patch('elasticsearch.Elasticsearch.ping')
    def test_health(self, mock_ping):
        response = self.app.get('/health')
        assert response.status == '200 OK'

    @mock.patch('elasticsearch.Elasticsearch.search')
    def test_get_one_auth_title(self, mock_es):
        mock_es.return_value = self.mock_result
        rv = self.app.get('auth/titles/' + self.test_title_number)
        assert self.test_title_number in rv.data

    @mock.patch('searchapi.es.Search.search')
    @mock.patch('searchapi.resources.abort')
    def test_404_auth_title(self, mock_abort, mock_search):
        mock_search.return_value = {'hits' : {}}
        response = self.app.get('auth/titles/' + self.test_title_number)
        mock_abort.assert_called_with(404, message="Title number %s not found" % self.test_title_number)
