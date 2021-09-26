import schedule
from expired_domain import check_domains
import time

schedule.every().day.do(check_domains)

while True:
    schedule.run_pending()
    time.sleep(1)