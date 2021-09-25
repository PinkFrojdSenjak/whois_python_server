from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)
 
class Data(Resource):
  def get(self):
    url = request.args.get('url')
    return {
      "naziv":url,
      "registar":'nestp randpm',
      
    }, 200

api.add_resource(Data, '/data')


if __name__ == '__main__':
  app.run(host = "0.0.0.0")
