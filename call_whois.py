import subprocess
import re
from hyperparameters import get_synonims, get_registry
import dateparser

registry = get_registry()
class Whois:
    def __init__(self, url) -> None:
        self.url = url
        args = self.url.split('.')
        self.domain = '.' + args[-1]
        self.command = 'whois'
        self._irrelevant_keys = ['notice', 'terms of use']

    def _process(self, args: list) -> str:
        p = subprocess.Popen(args, stdout= subprocess.PIPE, text = True)
        output, err = p.communicate()
        return output

    def get_raw(self) -> str:
        p = subprocess.Popen([self.command, self.url], stdout= subprocess.PIPE, text = True)
        output, err = p.communicate()
        return output

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
                    if important_field == 'Domain Name':
                        clean_dic[important_field] = self.url
                    elif important_field == 'Registration Date' or important_field == 'Expiration Date':
                        clean_dic[important_field] = str(dateparser.parse(dic[key]))
                    else:
                        clean_dic[important_field] = dic[key]
                    
                    found_synonim = True
                    break
            if not found_synonim: 
                non_synonim_fields[key] = dic[key]
        
        clean_dic['Registry'] = registry[self.domain]
        clean_dic['Registrant Name'] = ''
        clean_dic.update(non_synonim_fields)
        return clean_dic


    def extract_dict(self, s: str) -> dict:
        raw = s
        s = s.replace(':\n ', ': ')
        s = s.replace('Relevant dates:', '')
        s = s.replace('\t', ' ')
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
        
        reg = False
        adm = False
        tec = False
        for i, line in enumerate(lines):
            if ': ' in line:
                key, val = self._get_dict(line)
                if key.lower() == 'registrant':
                    reg = True
                if key.lower() == 'administrative contact':
                    adm = True
                if key.lower() == 'technical contact':
                    tec = True
                # only valid keys are maximum 3 words 
                if len(key.split()) <= 3 and key.lower() not in self._irrelevant_keys:
                    dic[key] = val
        if reg and adm and tec:
            return self.process_that_ours(lines)
                           
        return self._clean_dict_with_synonims(dic)

    def _no_match(self, s: str) -> bool:
        if 'no match' in s.lower() or 'not registered' in s.lower():
            return True
        return False

    def _not_domain(self, s: str) -> bool:
        if 'no whois server' in s.lower():
            return True
        return False

    def get_data(self) -> dict:
        """
        This method returns all Whois data for the given url
        """
        whois_return_string = self.get_raw()
        if whois_return_string is None:
            return None
        if self._no_match(whois_return_string):
            return {
                'url':self.url,
                'status':'free'
                }
        elif self._not_domain(whois_return_string):
            return {
                'url':self.url,
                'status':'unknown'
                }

        
        d = self.extract_dict(whois_return_string)
        d = self.process_foreign(d)
        try:
            d['Registrant Name'] = d['Registrant']['Registrant']
        except:
            pass
        d['status'] = 'active'
        return d

    def process_that_ours(self, lines: list) -> dict:
        prefix = ''
        dic = {}
        for i, line in enumerate(lines):
            key, val = self._get_dict(line)
            if key.lower() == 'registrant':
                prefix = 'Registrant '
            elif key.lower() == 'administrative contact':
                prefix = 'Administrative '
            elif key.lower() == 'technical contact':
                prefix = 'Technical '
            if key in ['Address', 'Postal Code', 'ID Number', 'Tax ID']:
                key = prefix + key
            if len(key.split()) <= 3 and key.lower() not in self._irrelevant_keys:
                dic[key] = val
        return self._clean_dict_with_synonims(dic)
        

    def process_foreign(self, dic: dict) -> dict:
        nested_fields = {
            'Registrant':{},
            'Admin':{},
            'Tech':{}
        }
        keys_for_deleting = []
        for f in nested_fields:
            for key in dic.keys():
                if f in key and f != key and key != 'Registrant Name':
                    try:
                        shortened_key = ' '.join(key.split()[1:])
                    except:
                        shortened_key = key.split()[-1]
                    nested_fields[f][shortened_key] = dic[key]
                    keys_for_deleting.append(key)
                elif f == key:
                    nested_fields[f][key] = dic[key]
        for key in keys_for_deleting:
            del dic[key]

        dic.update(nested_fields)
        return dic


if __name__ == '__main__':
    url = 'youtube.com'
    whois = Whois(url)
    res = whois.choose_service()
    dictionary = whois.extract_dict(res)
    temp = whois.get_data()
    print(dictionary)

    f = open('com.txt', 'w')
    f.write(res)
    f.close()