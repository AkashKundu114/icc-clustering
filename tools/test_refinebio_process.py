import requests
import time

ds_id = "588bed1a-ded0-4f96-859d-00f549c7352f"
url = f"https://api.refine.bio/v1/dataset/{ds_id}/"

# Get current data from dataset
cur = requests.get(url).json()

print(f"[*] Triggering processing for dataset {ds_id}...")
put_res = requests.put(url, json={
    "data": cur["data"],
    "aggregate_by": "EXPERIMENT",
    "scale_by": "NONE",
    "is_processed": True,
    "email_address": "akashkundu1152@gmail.com"
}, timeout=15)
print("PUT Status:", put_res.status_code)
print("PUT response:", put_res.json())

for _ in range(5):
    time.sleep(3)
    get_res = requests.get(url, timeout=15)
    data = get_res.json()
    print("Poll: is_processing =", data.get("is_processing"), "is_processed =", data.get("is_processed"), "is_available =", data.get("is_available"))
    if data.get("is_available"):
        print("Download URL:", data.get("download_url"))
        break
