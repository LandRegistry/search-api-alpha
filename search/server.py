from datetime import datetime
from elasticsearch import Elasticsearch

from flask import jsonify,request

from search import app

# by default we connect to localhost:9200
es = Elasticsearch()


@app.route('/', methods=['GET'])
def index():
    return 'OK!'


@app.route('/load', methods=['GET'])
def load():
    # datetimes will be serialized
    es.index(index="my_index", doc_type="titles", id=1,
             body={"title_number": "DN100", "timestamp": datetime.now(), "proprietor": "Matt Pease",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=2,
             body={"title_number": "DN101", "timestamp": datetime.now(), "proprietor": "Simon Tsang",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=3,
             body={"title_number": "DN103", "timestamp": datetime.now(), "proprietor": "Paul Trelease",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=4,
             body={"title_number": "DN104", "timestamp": datetime.now(), "proprietor": "Matt Shaw",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=5,
             body={"title_number": "DN105", "timestamp": datetime.now(), "proprietor": "Alan Hughes",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=6,
             body={"title_number": "DN106", "timestamp": datetime.now(), "proprietor": "Simon Chapman",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=7,
             body={"title_number": "DN107", "timestamp": datetime.now(), "proprietor": "Andy Porter",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=8,
             body={"title_number": "DN108", "timestamp": datetime.now(), "proprietor": "Simon Tsang",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})

    es.index(index="my_index", doc_type="titles", id=9,
             body={"title_number": "DN109", "timestamp": datetime.now(), "proprietor": "Simon Tsang",
                   "A-Register": "This is the A Register", "B-Register": "This is the B Register",
                   "C-Register": "This is the C Register"})
    # but not deserialized
    result = es.search(index="my_index", doc_type="titles", body={"query": {"match_all": {}}})

    return jsonify(result)


@app.route('/title/<title_no>', methods=['GET'])
def title(title_no):
    title_number = title_no

    raw_result = es.search(index="my_index", body={
        "query": {
            "match": {"title_number": title_number}
        }
    })

    hits = _get_hits(raw_result)
    return jsonify({'title': _get_item(hits[0])})


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()

    raw_result = es.search(index="my_index", body={
        "query": {
            "dis_max": {
                "tie_breaker": 0.7,
                "boost": 1.2,
                "queries": [
                    {"term": {"title_number": query}},
                    {"term": {"proprietor": query}}
                ]
            }
        }
    })

    hits = _get_hits(raw_result)
    return jsonify( {"results" : map(_get_item, hits) })


def _get_hits(raw_result):
    hits = raw_result.get('hits')
    return hits.get('hits')


def _get_item(raw_result):
    return raw_result.get("_source")
