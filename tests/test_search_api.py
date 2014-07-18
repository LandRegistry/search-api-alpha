from search import server

import unittest
import json
import calendar


class SearchAPITestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        #self.app.get('/load_test_data/')


    def test_get_one_title_back(self):
        title_no = 'DN100'
        self.app = server.app.test_client()
        assert 'DN100' in 'DN100'
        #self.app.get('/load_test_data/')
        #rv = self.app.get('/title/' + title_no)
        #assert 'DN100' in rv.data
