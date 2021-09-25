from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from call_whois import Whois


app = Flask(__name__)
api = Api(app)
 
class Data(Resource):
    def get(self):
        url = request.args.get('url')
        whois = Whois(url = url)
        data = whois.get_data()
        if data is None:
            return {}, 404
        else:
            return data, 200

api.add_resource(Data, '/data')


if __name__ == '__main__':
    app.run(host = "0.0.0.0")
