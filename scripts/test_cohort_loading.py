import sklearn.datasets
import numpy as np
import pandas as pd

openml_ids = {
    'breast_vantveer': 45088,
    'dlbcla': 45089,
    'ramaswamy': 45091,
    'novartis_bplc': 45095,
    'risinger': 45100,
    'su2001': 45103
}

for name, data_id in openml_ids.items():
    print(f"\nTesting {name} (OpenML ID {data_id})...", flush=True)
    try:
        ds = sklearn.datasets.fetch_openml(data_id=data_id, as_frame=True, parser='pandas')
        df_X = ds.data
        s_y = ds.target
        print(f"  Success: shape={df_X.shape}, target_unique={s_y.nunique()}, target_counts={dict(s_y.value_counts().head(3))}", flush=True)
    except Exception as e:
        print(f"  Failed: {e}", flush=True)
