import subprocess
import re

class Whois:
    def __init__(self, url) -> None:
        self.url = url

    def choose_service(self):
        if re.findall(r'.rs', self.url):
            self.process_serbian()
        

    def process_serbian(self):
        service = 'https://www.rnids.rs/en/whois'
        

url = "https://donosimo.rs/"


if __name__ == '__main__':
    url = "https://donosimo.rs/"
    