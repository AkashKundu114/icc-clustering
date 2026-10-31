import pandas as pd

df = pd.read_csv("results/stability_degeneracy_audit.csv")
pts = df[~df["is_control"] & (df["acc"] <= 0.08) & (df["stab"] >= 0.45)]
print(pts[["dataset", "model", "stab", "acc"]])
