import subprocess
import re

class Whois:
    def __init__(self, url) -> None:
        self.url = url
        self.command = 'whois'

    def _process(self, args: list) -> str:
        p = subprocess.Popen(args, stdout= subprocess.PIPE, text = True)
        output, err = p.communicate()
        return output

    def choose_service(self) -> str:
        if re.findall(r'.rs', self.url) or re.findall(r'.срб', self.url):
            return self.process_serbian()

        elif re.findall(r'.ru', self.url) or re.findall(r'.рф', self.url):
            return self.process_russian()

        elif re.findall(r'.mk', self.url) or re.findall(r'.мкд', self.url):
            return self.process_makedonian()

        elif re.findall(r'.org', self.url) or re.findall(r'.opr', self.url):
            return self.process_org_opr()

        elif re.findall(r'.com', self.url):
            return self.process_com()

        elif re.findall(r'.ком', self.url): 
            return self.process_kom()
        
        elif re.findall(r'.net', self.url):
            return self.process_net()

        elif re.findall(r'.uk', self.url):
            return self.process_uk()

        elif re.findall(r'.se', self.url):
            return self.process_se()

    def process_serbian(self) -> str:
        service = 'whois.rnids.rs'
        return self._process([self.command, '-h', service, self.url])

    def process_russian(self) -> str:
        service = 'whois.tcinet.ru'
        return self._process([self.command, '-h', service, self.url])
    
    def process_makedonian(self) -> str:
        service = 'whois.marnet.mk'
        return self._process([self.command, '-h', service, self.url])

    def process_org_opr(self) -> str:
        service = 'whois.publicinterestregistry.net'
        return self._process([self.command, '-h', service, self.url])

    def process_com(self) -> str:
        service = 'whois.verisign-grs.com'
        return self._process([self.command, '-h', service, self.url])

    def process_kom(self) -> str:
        service = 'whois.nic.ком'
        return self._process([self.command, '-h', service, self.url])

    def process_net(self) -> str:
        service = 'whois.verisign-grs.com'
        return self._process([self.command, '-h', service, self.url])

    def process_uk(self) -> str:
        service = 'whois.nic.uk'
        return self._process([self.command, '-h', service, self.url])

    def process_se(self) -> str:
        service = 'whois.iis.se'
        return self._process([self.command, '-h', service, self.url])

    def _get_dict_entries(self, line):
        key, val = line.split(': ')
        key = key.lstrip().rstrip()
        val = val.lstrip().rstrip()
        return key, val

    def extract_dict(self, s: str) -> dict:
        lines = s.splitlines()
        dic = {}
        for line in lines:
            if ': ' in line:
                key, val = self._get_dict_entries(line)                
                dic[key] = val
        return dic
        
if __name__ == '__main__':
    url = 'bbc.co.uk'
    whois = Whois(url)
    res = whois.choose_service()
    dictionary = whois.extract_dict(res)
    print(dictionary)

    f = open('uk.txt', 'w')
    f.write(res)
    f.close()