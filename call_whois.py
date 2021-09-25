import subprocess
import re
from variable_synonims import get_synonims

class Whois:
    def __init__(self, url) -> None:
        self.url = url
        self.command = 'whois'
        self._irrelevant_keys = ['notice', 'terms of use']

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
        else:
            return None

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

    def _get_dict(self, line: str) -> tuple:
        key, val = line.split(': ', maxsplit = 1)
        key = key.lstrip().rstrip()
        val = val.lstrip().rstrip()
        return key, val

    def _clean_dict_with_synonims(self, dic: dict) -> dict:
        """
        This method takes the unsorted dictionary and check to see if there are known synonims 
        for some of the most important fields and also places first 
        """
        clean_dic = {}
        synonims = get_synonims()
        non_synonim_fields = {}
        for key in dic.keys():
            found_synonim = False
            for important_field in synonims.keys():
                if key.lower() in synonims[important_field]:
                    clean_dic[important_field] = dic[key]
                    found_synonim = True
                    break
            if not found_synonim: 
                non_synonim_fields[key] = dic[key]

        for key in non_synonim_fields.keys():
            clean_dic[key] = non_synonim_fields[key]
        return clean_dic

    def extract_dict(self, s: str) -> dict:
        s = s.replace(':\n ', ': ')
        s = s.replace('Relevant dates:', '')
        lines = s.splitlines()
        # remove empty lines and lines that start with %
        temp = []
        for line in lines:
            if line and line[0] != '%':
                temp.append(line)
        lines = temp
        temp = []
        # get only relevant data
        dic = {}
        for i, line in enumerate(lines):
            if ': ' in line:
                key, val = self._get_dict(line) 
                # only valid keys are maximum 3 words 
                if len(key.split()) <= 3 and key.lower() not in self._irrelevant_keys:
                    dic[key] = val
            
                           
        return self._clean_dict_with_synonims(dic)

    def get_data(self) -> dict:
        whois_return_string = self.choose_service()
        if whois_return_string is None:
            return None
        return self.extract_dict(whois_return_string)

if __name__ == '__main__':
    url = 'aaa'
    whois = Whois(url)
    res = whois.choose_service()
    dictionary = whois.extract_dict(res)
    print(dictionary)

    f = open('com.txt', 'w')
    f.write(res)
    f.close()