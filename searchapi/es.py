from elasticsearch import Elasticsearch

from searchapi import app


def _get_hits(raw_result):
    hits = raw_result.get('hits')
    return hits.get('hits')


def _get_item(raw_result):
    return raw_result.get("_source")


class Search(object):

    def __init__(self):
        # Connect to the host and port as defined in the config
        # (which in turn come from the OS environment)
        self.es = Elasticsearch([{
          'host': app.config['ELASTICSEARCH_HOST'],
          'port': app.config['ELASTICSEARCH_PORT'],
          'use_ssl': app.config['ELASTICSEARCH_USESSL'],
          'http_auth': app.config['ELASTICSEARCH_USERPASS']}])

    def get(self, query):
        app.logger.info("Searching for %s on Elastic Search %s" %
            (query, app.config['ELASTICSEARCH_HOST']))


        raw_result = self.es.search(index="public_titles", body={
            "query":{
                "multi_match": {
                "query": query,
                "fields": ["title_number", "postcode"]
            }
            }
        })

        hits = _get_hits(raw_result)
        result = map(_get_item, hits)
        return result

    def search(self, **kwargs):
        return self.es.search(**kwargs)

    def index(self, **kwargs):
        return self.es.index(**kwargs)

    def health(self):
        try:
            self.es.ping()
            return True, "ElasticSearch"
        except:
            return False, "ElasticSearch"
