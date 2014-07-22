from elasticsearch import Elasticsearch
from flask import jsonify, request, Response

from search import app

# Connect to the host and port as defined in the config (which in turn come from the OS environment)
es = Elasticsearch([
    {'host': app.config['ELASTICSEARCH_HOST'], 'port': app.config['ELASTICSEARCH_PORT'],
    'use_ssl': app.config['ELASTICSEARCH_USESSL'], 'http_auth': app.config['ELASTICSEARCH_USERPASS']}
])

@app.route('/', methods=['GET'])
def index():
    return 'OK!'


#TODO How about a Blueprint to separate out the
# management endpoints (load, clear etc) and
# and the query endpoints?

#TODO maybe lock down this url :)
@app.route('/clear', methods=['GET'])
def clear():
    es.indices.delete(index='*')
    return 'ElasticSearch cleared'


@app.route('/load/<string:index>' , methods=['PUT'])
def load_title(index):
    json = request.json
    app.logger.info("Load request for data %s and index %s" % (json, index))
    if json:
        es.index(index=index, doc_type="titles", body=json)
        return Response(status = 201)
    else:
        return Response(status = 400)


# Time to remove these?
@app.route('/load_test_data', methods=['GET'])
def load():
    # datetimes will be serialized
    es.indices.delete(index='*')
    es.indices.create(index="public_titles")
    es.indices.refresh(index="public_titles")
    es.index(index="public_titles", doc_type="titles", id=1,
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

    es.index(index="public_titles", doc_type="titles", id=2,
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

    es.index(index="public_titles", doc_type="titles", id=3,
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
    result = es.search(index="public_titles", doc_type="titles", body={"query": {"match_all": {}}})
    return jsonify(result)

#NOTE : Alternative to the above view function below
from search.resources import PublicTitleResource, AuthenticatedTitleResource
from flask.ext.restful import Api
api = Api(app)
api.add_resource(PublicTitleResource, '/titles/<string:title_number>')

#This will be moved to anothe api server asap
api.add_resource(AuthenticatedTitleResource, '/auth/titles/<string:title_number>')

# instead of this
# @app.route('/titles/<title_number>', methods=['GET'])
# def title(title_number):
#     app.logger.info("Search for title number %s" % title_number)
#     raw_result = es.search(index="my_index", body={
#         "query": {
#             "match": {"title_number": title_number}
#         }
#     })

#     hits = _get_hits(raw_result)
#     if hits:
#         return jsonify({'title': _get_item(hits[0])})
#     else:
#         return abort(404)


@app.route('/search', methods=['GET'])
def search():
    #need some logging on method like this
    query = request.args.get('query')

    app.logger.info("Searching for %s on Elastic Search %s" % (query, app.config['ELASTICSEARCH_HOST']))

    raw_result = es.search(index="public_titles", body={
        "query": {
            "multi_match" : { # once we get more complicated we may need to merge multiple query types, until then, this will do
                "query":      query,
                "type":       "phrase_prefix", # best_fields seems to do full matching only
                "fields":     [ "title_number^3", "first_name", "last_name^2" ]
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
