from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

import json

app = Flask(__name__)
api = Api(app)

class Health(Resource):
    def get(self):
        return {'status': 'up'}

api.add_resource(Health, '/health')

class Event(Resource):
    def post(self):
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Request: %s', request.get_data())

        entry = json.loads(request.get_data().decode())
        
        with open('queue.json', '+r') as file:
            file_data = json.load(file)
            file_data['queue'].append(entry)
            file.seek(0)
            json.dump(file_data, file, indent = 2)
        return ('', 202)

api.add_resource(Event, '/hello/world/event')

if __name__ == '__main__':
    app.run(debug=True)