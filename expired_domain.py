from os import curdir
import sqlite3
from call_whois import Whois
import firebase_admin
from firebase_admin import messaging

con = sqlite3.connect('notifications.db', check_same_thread=False)
curr = con.cursor()

def get_domains():
    curr.execute('SELECT DISTINCT url FROM Subscriptions')
    urls = curr.fetchall()
    urls = [x[0] for x in urls]
    return urls

def send_notifications(data, t):
    curr.execute('SELECT DISTINCT email FROM Subscriptions WHERE url = ? AND email IS NOT NULL', (data['Domain Name'], ))
    rows = curr.fetchall()
    emails = [x[0] for x in rows]

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