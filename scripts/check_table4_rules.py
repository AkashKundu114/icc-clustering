import pandas as pd

df = pd.read_csv("results/stability_degeneracy_audit.csv")
non_control = df[~df["is_control"]].copy()

print("--- PROSTATE CELL ANALYSIS ---")
prostate = non_control[non_control["dataset"] == "prostate"].sort_values("model")
for idx, r in prostate.iterrows():
    m = r["model"]
    s = r["stab"]
    a = r["acc"]
    dr = r["degen_rate"] * 100
    mf = r["mean_min_frac"] * 100
    r1 = r["rule_i"]
    r1p = r["rule_i_prime"]
    print(f"  {m:12s}: stab={s:.3f}, acc={a:+.3f}, degen={dr:5.1f}%, min_frac={mf:5.1f}%, Rule(i)={r1}, Rule(i')={r1p}")

print("\n--- ALL COHORTS: RULES MET COUNT PER MODEL ---")
models = non_control["model"].unique()
for m in models:
    m_df = non_control[non_control["model"] == m]
    r1_count = m_df["rule_i"].sum()
    r1p_count = m_df["rule_i_prime"].sum()
    r1p_cohorts = m_df[m_df["rule_i_prime"]]["dataset"].tolist()
    r1_cohorts = m_df[m_df["rule_i"]]["dataset"].tolist()
    print(f"  {m:12s}: Rule(i)={r1_count}/6 (cohorts: {r1_cohorts}), Rule(i')={r1p_count}/6 (cohorts: {r1p_cohorts})")
