import subprocess
import re

class Whois:
    def __init__(self, url) -> None:
        self.url = url

    def choose_service(self):
        if re.findall(r'.rs', self.url):
            return self.process_serbian()
        
    def process_serbian(self):
        service = 'whois.rnids.rs'
        command = 'whois'
        p = subprocess.Popen([command,'-h', service, self.url], stdout= subprocess.PIPE, text = True)
        output, err = p.communicate()
        return output



if __name__ == '__main__':
    url = "donosimo.rs"
    whois = Whois(url)
    print(whois.choose_service())