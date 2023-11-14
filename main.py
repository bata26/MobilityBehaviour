from pandas import read_csv
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        data = read_csv('data/preprocessedDataset.csv')
        data = data.to_dict()
        return {'data': data}, 200
    def post(self):
        some_json = request.get_json()
        return {'you sent ': some_json}, 201
api.add_resource(HelloWorld, '/')

class Multi(Resource):
    def get(self, num):
        return {'result ': num * 10}
api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
