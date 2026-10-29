import requests
import re

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

r = s.get('https://www.gptinf.com/ai-detector')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)

for sc in scripts:
    if sc.startswith('http'):
        continue
    url = 'https://www.gptinf.com' + sc.split('?')[0]
    try:
        r_sc = s.get(url, timeout=5)
        if 'detect' in r_sc.text.lower() and ('api' in r_sc.text.lower() or 'score' in r_sc.text.lower()):
            endpoints = set(re.findall(r'/api/[a-zA-Z0-9_\-/]+', r_sc.text))
            if endpoints:
                print(f'Script {sc} has endpoints: {endpoints}')
    except Exception as e:
        pass
