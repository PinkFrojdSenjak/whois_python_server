from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)
 #enter postman and use get request for  http://127.0.0.1:5000/users
 
class Data(Resource):
  def get(self):
    url = request.args.get('url')
    return {
      "sample":[1,2,3],
      "data":[4,3,5],
      'url':url
    }, 200

api.add_resource(Data, '/data')


if __name__ == '__main__':
  app.run(host = "0.0.0.0")
