

from flask import jsonify, request, Response

from .health import Health

from searchapi import app
from searchapi.es import Search

es = Search()
Health(app, checks=[es.health])


@app.route('/', methods=['GET'])
def index():
    return 'OK!'


@app.route('/load/<string:index>', methods=['PUT'])
def load_title(index):
    json = request.json
    app.logger.info("Load request for data %s and index %s" % (json, index))
    if json:
        es.index(index=index, doc_type="titles", body=json, id=json['title_number'])
        return Response(status=201)
    else:
        return Response(status=400)

#TODO How about a Blueprint to separate out the
# management endpoints (load, clear etc) and
# and the query endpoints?


#NOTE : Alternative to the above view function below
from searchapi.resources import PublicTitleResource, AuthenticatedTitleResource
from flask.ext.restful import Api
api = Api(app)
api.add_resource(PublicTitleResource, '/titles/<string:title_number>')

#This will be moved to another api server asap
api.add_resource(AuthenticatedTitleResource, '/auth/titles/<string:title_number>')


@app.route('/search', methods=['GET'])
def search():
    #need some logging on method like this
    query = request.args.get('query').lower()

    result = es.get(query)
    return jsonify({"results": result})
