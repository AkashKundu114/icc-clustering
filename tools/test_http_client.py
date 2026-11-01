import http.client
import ssl

context = ssl.create_default_context()
conn = http.client.HTTPSConnection("ftp.ncbi.nlm.nih.gov", context=context, timeout=10)
conn.request("GET", "/geo/series/GSE49nnn/GSE49710/matrix/GSE49710_series_matrix.txt.gz")
res = conn.getresponse()
print("Status:", res.status, res.reason)
print("Headers:", res.getheaders())
chunk = res.read(1024)
print("Read chunk size:", len(chunk))
conn.close()
