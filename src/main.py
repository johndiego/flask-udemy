from os import environ

from flask import Flask, request
from flask_restful import Resource, Api
from pdb import set_trace as debug

FLASK_PORT = environ.get('FLASK_PORT')

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):

    def get(self, name):
        for item in items:
            if item.get('name') == name:
                return item
        return {'message': 'item not found u.u'}, 404

    def post(self, name):
        # Fails if does not have a payload or the ContentType header is not set
        # Can be bypassed with the force flag, but always executes it
        # Also, the silent flag can help not to rise an error
        payload = request.get_json(silent=True)
        item = {'name': name, 'price': payload.get('price')}
        items.append(item)
        return item, 201

class ItemList(Resource):
    
    def get(self):
        return {'items': items}

if __name__ == '__main__':
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    app.run(port=FLASK_PORT, host='0.0.0.0')