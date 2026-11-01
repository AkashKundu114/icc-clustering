import requests

url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE49nnn/GSE49710/matrix/GSE49710_series_matrix.txt.gz"
headers = {"Range": "bytes=0-1048575"}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print("Status:", r.status_code)
    print("Content-Range:", r.headers.get("Content-Range"))
    print("Content-Length:", r.headers.get("Content-Length"))
    print("Received bytes:", len(r.content))
except Exception as e:
    print("Error:", e)
