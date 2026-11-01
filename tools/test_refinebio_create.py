import json
import time
import urllib.request
import requests

BASE_URL = "https://api.refine.bio/v1"

def create_dataset_for_experiment(accession):
    print(f"[*] Fetching sample list for {accession} from refine.bio...")
    exp_res = requests.get(f"{BASE_URL}/experiments/{accession}/", timeout=15)
    exp_res.raise_for_status()
    exp_data = exp_res.json()
    
    samples = [s["accession_code"] for s in exp_data.get("samples", []) if s.get("is_processed")]
    print(f"[+] Found {len(samples)} processed samples for {accession}.")
    
    payload = {
        "data": {
            accession: samples
        },
        "aggregate_by": "EXPERIMENT",
        "scale_by": "NONE",
        "email_address": "akashkundu1152@gmail.com"
    }
    
    print(f"[*] Posting dataset creation request...")
    ds_res = requests.post(f"{BASE_URL}/dataset/", json=payload, timeout=20)
    print("Response status:", ds_res.status_code)
    print("Response json:", ds_res.json())
    return ds_res.json()

if __name__ == "__main__":
    create_dataset_for_experiment("GSE31210")
