from flask.ext.restful import Resource, fields, marshal_with, reqparse, abort

from search.server import app, es

def get_hits(raw_result):
    hits = raw_result.get('hits')
    return hits.get('hits')

def get_item(raw_result):
    return raw_result.get("_source")

class PublicTitleResource(Resource):

    public_title_fields = { 'title_number':   fields.String,
                                    'house_number':   fields.String,
                                    'road':   fields.String,
                                    'town':   fields.String,
                                    'postcode':   fields.String,
                                    'price_paid':   fields.String}

    def __init__(self):
        self.parser = reqparse.RequestParser()
        for key, val in PublicTitleResource.public_title_fields.items():
            self.parser.add_argument(key, type=str)

    @marshal_with(public_title_fields)
    def get(self, title_number):
        app.logger.info("Search for title number %s" % title_number)
        raw_result = es.search(index="public_titles", body={
            "query": {
            "match": {"title_number": title_number}
            }
        })
        hits = get_hits(raw_result)
        if hits:
            title = get_item(hits[0])
            app.logger.info('Found title %s' % title)
            return title
        else:
            abort(404, message="Title number %s not found" % title_number )


class AuthenticatedTitleResource(Resource):

    name_fields = {
        'first_name' : fields.String,
        'last_name' : fields.String
    }

    address_fields = {  'house_number' :  fields.String,
                                    'road' :  fields.String,
                                    'town' :  fields.String,
                                    'postcode' :  fields.String
    }

    payment_fields = {
           'titles' : fields.List(fields.String),
           'price_paid': fields.Integer
    }

    property_fields = {
         'address': fields.Nested(address_fields),
        'class_of_title'  :  fields.String,
        'tenure' : fields.String,
    }

    title_fields = {
        'proprietors'  :  fields.Nested(name_fields),
        'title_number'  :  fields.String,
        'property'  :  fields.Nested(property_fields),
        'payment' :  fields.Nested(payment_fields),
    }

    @marshal_with(title_fields)
    def get(self, title_number):
        app.logger.info("Search for title number %s" % title_number)
        raw_result = es.search(index="authenticated_titles", body={
            "query": {
            "match": {"title_number": title_number}
            }
        })
        hits = get_hits(raw_result)
        if hits:
            title = get_item(hits[0])
            app.logger.info('Found title %s' % title)
            return title
        else:
            abort(404, message="Title number %s not found" % title_number )



