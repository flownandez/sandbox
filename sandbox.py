from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask import json, jsonify

app = Flask(__name__)
api = Api(app)

TRIPLETS = {
    'triplet1': {'task': 'build an API'},
    'triplet2': {'task': '?????'},
    'triplet3': {'task': 'profit!'},
}

def abort_if_triplet_doesnt_exist(triplet_id):
    if triplet_id not in TRIPLETS:
        abort(404, message="Triplit {} doesn't exist".format(triplet_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

# Triplet
#   show a single triplet item and lets you delete them
class Triplet(Resource):
    def get(self, triplet_id):
        abort_if_triplet_doesnt_exist(triplet_id)
        return TRIPLETS[triplet_id]

    def delete(self, triplet_id):
        abort_if_triplet_doesnt_exist(triplet_id)
        del TRIPLETS[triplet_id]
        return '', 204

    def put(self, triplet_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TRIPLETS[triplet_id] = task
        return task, 201

# TripletList
#   shows a list of all triplets, and lets you POST to add new tasks
class TripletList(Resource):
    def get(self):
        return TRIPLETS

    def post(self):
        args = parser.parse_args()
        triplet_id = 'triplet%d' % (len(TRIPLETS) + 1)
        TRIPLETS[triplet_id] = {'task': args['task']}
        return TRIPLETS[triplet_id], 201

## Setup the Api resource routing here
api.add_resource(TripletList, '/triplets')
api.add_resource(Triplet, '/triplets/<string:triplet_id>')

if __name__ == '__main__':
    app.run(debug=True)