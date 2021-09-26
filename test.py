import datetime
import dateparser

today = datetime.datetime.now()

earlier = dateparser.parse('24/09/2021')

print(type((today - earlier).days))