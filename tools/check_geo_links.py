import urllib.request
import re

url = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE62254'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print(html[:2000])
