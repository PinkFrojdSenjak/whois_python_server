from os import curdir
import sqlite3
from call_whois import Whois
import firebase_admin
from firebase_admin import messaging
import requests
import json

con = sqlite3.connect('notifications.db', check_same_thread=False)
curr = con.cursor()

def get_domains():
    curr.execute('SELECT DISTINCT url FROM Subscriptions')
    urls = curr.fetchall()
    urls = [x[0] for x in urls]
    return urls

def send_notifications(data, t):
    curr.execute('SELECT DISTINCT email,id FROM Subscriptions WHERE url = ? AND email IS NOT NULL', (data['Domain Name'], ))
    rows = curr.fetchall()
    #emails = [x[0] for x in rows]

    for email,id in rows:
        print(email,id)
        post_data = {
            "salje": {
                "adresa": "whoishakaton@geasoft.net",
                "ime": "Ko.Je Domen Alarm"
            },
            "prima": [{
                "adresa": email,
                "ime": "" 
            }],
            "naslov": f"Alarm za domen {data['Domain Name']}",
            "sadrzaj": f"Domen istice za {t} dana."
            }
        #if t == 0:
        with open('email.html', 'r') as f:
            s = f.read()
            s=s.replace("$url",data['Domain Name'])
            s=s.replace("$dana",str(t))
            s=s.replace("$id", id)
            post_data['sadrzaj'] = s
        x = requests.post("http://whois-emailer.geasoft.net", data = json.dumps(post_data), headers= {"Content-Type":"application/json"})
        
        
    curr.execute('SELECT DISTINCT token FROM Subscriptions WHERE url = ? AND token IS NOT NULL', (data['Domain Name'], ))
    rows = curr.fetchall()
    tokens = [x[0] for x in rows]

    for token in tokens:
        message_info = {
                "title":f"Alarm za domen {data['Domain Name']}",
                "message":f"Domen istice za {t} dana."
            }
        if t == 0:
            message_info['message'] = 'Domen je istekao!'
        message = messaging.Message(
            data=message_info,
            token=token,
            )
        messaging.send(message)

def check_domains(threshold = [0,1,3,7,10]):
    urls = get_domains()
    for url in urls:
        w = Whois(url)
        data = w.get_data()
        for t in threshold:
            try:
                if data['Expires in'] == t:
                    send_notifications(data, t)
            except:
                pass
def check_domains_mock():
    urls = get_domains()
    for url in urls:
        w = Whois(url)
        data = w.get_data()
        send_notifications(data, data['Expires in'])

if __name__ == '__main__':
    print(get_domains())