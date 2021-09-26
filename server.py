from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from call_whois import Whois
from dig import dns


app = Flask(__name__)
api = Api(app)
 
class Data(Resource):
    def get(self):
        url = request.args.get('url')
        args = url.split('.')
        domain = '.' + args[-1]
        whois = Whois(url = url)
        data = whois.get_data()
        dns_data = dns(url)
        data['dns'] = dns_data
         
        if data is None or not data:
            return {}, 404
        else:
            return data, 200


api.add_resource(Data, '/data')


if __name__ == '__main__':
    app.run(host = "0.0.0.0")
