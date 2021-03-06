from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from call_whois import Whois
from dig import dns
import firebase_admin
from firebase_admin import messaging
import os
from notification_database import Notifications
from expired_domain import check_domains, check_domains_mock
from flask import Response

with open("privateKeyPath.txt", "r") as f:
    path = f.read()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path

app = Flask(__name__)
api = Api(app)
default_app = firebase_admin.initialize_app()
nots = Notifications()
class Data(Resource):
    def get(self):
        url = request.args.get('url')
        whois = Whois(url = url)
        data = whois.get_data()
        dns_data = dns(url)
        data['dns'] = dns_data

        if data is None or not data:
            return {}, 404
        else:
            return data, 200
class Subscribe(Resource):
    def get(self):
        url = request.args.get('url')
        email = request.args.get('email')
        token = request.args.get('token')
        if nots.subscribe(url, email, token):
            return {'status':'ok'}
        else:
            return {'status':'err'}

class UnsubscribePush(Resource):
    def get(self):
        token = request.args.get('token')
        nots.unsubscribe_push(token)

class UnsubscribeEmail(Resource):
    def get(self):
        id = request.args.get('id')
        nots.unsubscribe_email(id)
        return Response("<h1> Uspešno ste se odjavili.", mimetype='text/html')
class ChangeToken(Resource):
    def get(self):
        old = request.args.get('old')
        new = request.args.get('new')
        nots.change_token(old, new)

class SendAll(Resource):
    def get(self):
        check_domains_mock()


api.add_resource(Data, '/data')
api.add_resource(Subscribe, '/subscribe')
api.add_resource(UnsubscribePush, '/unsubscribe-push')
api.add_resource(UnsubscribeEmail, '/unsubscribe-email')
api.add_resource(ChangeToken, '/change-token')
api.add_resource(SendAll, '/send-all')

if __name__ == '__main__':
    print(default_app.name)
    app.run(host = "0.0.0.0")
    