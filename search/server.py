from elasticsearch import Elasticsearch
from flask import jsonify, request, abort, Response

from search import app

# by default we connect to localhost:9200
es = Elasticsearch()


@app.route('/', methods=['GET'])
def index():
    return 'OK!'

@app.route('/clear', methods=['GET'])
def clear():
    es.indices.delete(index='*')
    return 'ElasticSearch cleared'


@app.route('/load' , methods=['PUT'])
def load_title():
    json = request.json
    if json:
        es.index(index="my_index", doc_type="titles", body=json)
        return Response(status = 201)
    else:
        return Response(status = 400)

@app.route('/load_test_data', methods=['GET'])
def load():
    # datetimes will be serialized
    es.indices.delete(index='*')
    es.indices.create(index="my_index")
    es.indices.refresh(index="my_index")
    es.index(index="my_index", doc_type="titles", id=1,
             body={
                'title_number': "DN100",
                'proprietors': [
                    {
                        'first_name': "Simon",
                        'last_name': "Tsang"
                    },
                    {
                        'first_name': "Matt",
                        'last_name': "Pease"
                    }
                ],
                'property' : {
                    'address': {
                        'line_1': "1 High Street",
                        'line_2': "Croydon",
                        'postcode': "CR0 0NN",
                    },
                    'tenure': "freehold",
                    'class_of_title': "absolute",
                },
                'payment': {
                    'price_paid': "1234500",
                    'titles': ["DN100"]
                }
            })

    es.index(index="my_index", doc_type="titles", id=2,
             body={
                'title_number': "DN101",
                'proprietors': [
                    {
                        'first_name': "Simon",
                        'last_name': "Chapman"
                    }
                ],
                'property' : {
                    'address': {
                        'line_1': "13 High Street",
                        'line_2': "Croydon",
                        'postcode': "CR0 1NN",
                    },
                    'tenure': "freehold",
                    'class_of_title': "absolute",
                },
                'payment': {
                    'price_paid': "12500",
                    'titles': ["DN101"]
                }
            })

    es.index(index="my_index", doc_type="titles", id=3,
             body={
                'title_number': "DN102",
                'proprietors': [
                    {
                        'first_name': "Matt",
                        'last_name': "Shaw"
                    }
                ],
                'property' : {
                    'address': {
                        'line_1': "13 Low Street",
                        'line_2': "Croydon",
                        'postcode': "CR2 1NN",
                    },
                    'tenure': "leasehold",
                    'class_of_title': "absolute",
                },
                'payment': {
                    'price_paid': "12500",
                    'titles': ["DN102"]
                }
            })
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
    if hits:
        return jsonify({'title': _get_item(hits[0])})
    else:
        return abort(404)


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
                    {"term": {"first_name": query}},
                    {"term": {"last_name": query}}
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
