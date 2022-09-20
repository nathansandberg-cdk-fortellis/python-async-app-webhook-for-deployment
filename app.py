from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

import json

import jwt
from jwt import PyJWKClient

PREFIX = 'Bearer '

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

        token = request.headers['Authorization'][len(PREFIX):]

        url = "https://identity.fortellis.io/oauth2/aus1p1ixy7YL8cMq02p7/v1/keys"

        jwks_client = PyJWKClient(url)

        signing_key = jwks_client.get_signing_key_from_jwt(token)

        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api_providers",
            subject="{yourAPIKey}",
            options={"verify_exp": True},
        )

        print(data)

        entry = json.loads(request.get_data().decode())  

        with open('queue.json', '+r') as file:
            file_data = json.load(file)
            file_data['queue'].append(entry)
            file.seek(0)
            json.dump(file_data, file, indent = 2)
        return ('', 202)

api.add_resource(Event, '/event/hello/world')

class Queue(Resource):
    def get(self):
        with open('queue.json', '+r') as file:
            file_data = json.load(file)
            
        return file_data

api.add_resource(Queue, '/event/hello/world')

if __name__ == '__main__':
    app.run(debug=True)