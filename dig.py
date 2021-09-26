import subprocess

def clean_data(s: str) -> str:
    s = s.replace('\t', ' ')
    lines = s.splitlines()
    clean_lines = []
    for line in lines:
        if line and line[0] != ';':
            clean_lines.append(line)
    if len(clean_lines) == 1:
        answer = clean_lines[0].split(maxsplit = 4)
        return answer[-1].lstrip().rstrip()
    else:
        answer = clean_lines[1:]
        answer = [x.split(maxsplit = 4) for x in answer]
        return [x[-1].lstrip().rstrip() for x in answer]

    

def dns(url):
    p = subprocess.Popen(['dig', url], stdout=subprocess.PIPE, text=True)
    a, err = p.communicate()
    a = clean_data(a)
    p = subprocess.Popen(['dig', url,'AAAA'], stdout=subprocess.PIPE, text=True)
    aaaa, err = p.communicate()
    aaaa = clean_data(aaaa)
    p = subprocess.Popen(['dig', url, 'MX'], stdout=subprocess.PIPE, text=True)
    mx, err = p.communicate()
    mx = clean_data(mx)
    p = subprocess.Popen(['dig', url, 'NS'], stdout=subprocess.PIPE, text=True)
    ns, err = p.communicate()
    ns = clean_data(ns)
    data = {
        'a':a,
        'aaaa': aaaa,
        'mx': mx,
        'ns':ns
    }
    return data

if __name__ == '__main__':
    data = dns('google.com')
    print(data)