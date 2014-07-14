from datetime import datetime
from elasticsearch import Elasticsearch

from flask import jsonify,  abort, request, make_response

from search import app

# by default we connect to localhost:9200
es = Elasticsearch()

@app.route('/', methods=['GET'])
def index():



    # datetimes will be serialized
    es.index(index="my_index", doc_type="titles", id=42, body={"any": "data", "timestamp": datetime.now()})
    {u'_id': u'42', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}

    # but not deserialized
    foo = es.get(index="my_index", doc_type="titles", id=42)['_source']
    {u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}
    print foo
    return "OK"
