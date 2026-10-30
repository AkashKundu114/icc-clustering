"""
scripts/audit_degeneracy.py

Executes Item 2b, 2c, 2d:
- Computes mean number of non-empty clusters, mean smallest-cluster fraction,
  mean largest-cluster fraction, and degenerate fraction (smallest cluster < 5%)
  for every method x cohort.
- Computes reference controls:
  (i) Constant / near-constant partition (one singleton outlier)
  (ii) Random balanced partition with true class sizes
- Evaluates Rule (i) vs amended Rule (i').
- Recomputes Rule (iii) paired bootstrap (B=10000, fixed seed) with and without exclusion of degenerate pairs.
"""

from itertools import combinations
from pathlib import Path
from icc.datasets.registry import load_dataset
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

ROOT = Path(__file__).resolve().parent.parent
PARTITIONS_DIR = ROOT / "results" / "stability" / "partitions"
DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
MODELS = [
    "K-Means", "Ward", "Spectral", "FCM", "StdCons", "CoreHalo",
    "FCAG", "FastMVC", "CoHiRF", "UngatedAC", "GAC", "DEC"
]

def main():
    records = []

    for d in DATASETS:
        X, y, meta = load_dataset(d)
        k_target = meta["K"]
        n_total = len(y)

        # -------------------------------------------------------------
        # 1. Reference Controls (Item 2c)
        # -------------------------------------------------------------
        # Control (i): Near-constant (one sample in cluster 1, rest in 0)
        near_const_parts = []
        near_const_accs = []
        # Control (ii): Random balanced partition matching true class sizes
        rand_bal_parts = []
        rand_bal_accs = []

        # We load subsample indices from an existing model's files
        for sub_id in range(30):
            sample_pfile = PARTITIONS_DIR / f"{d}_GAC_real_{sub_id}.npy"
            if not sample_pfile.exists():
                sample_pfile = PARTITIONS_DIR / f"{d}_K-Means_real_{sub_id}.npy"
            sdata = np.load(sample_pfile, allow_pickle=True).item()
            sub_idx = sdata["sub_idx"]
            n_sub = len(sub_idx)

            # Near-constant
            lbl_nc = np.zeros(n_sub, dtype=int)
            lbl_nc[0] = 1
            near_const_parts.append((sub_idx, lbl_nc))
            near_const_accs.append(adjusted_rand_score(y[sub_idx], lbl_nc))

            # Random balanced (permute true labels of subsample)
            rng = np.random.default_rng(7000 + sub_id)
            lbl_rb = rng.permutation(y[sub_idx])
            rand_bal_parts.append((sub_idx, lbl_rb))
            rand_bal_accs.append(adjusted_rand_score(y[sub_idx], lbl_rb))

        def calc_stab(parts):
            aris = []
            for i, j in combinations(range(len(parts)), 2):
                idx_i, lbl_i = parts[i]
                idx_j, lbl_j = parts[j]
                shared = np.intersect1d(idx_i, idx_j)
                if len(shared) >= 2:
                    map_i = {val: pos for pos, val in enumerate(idx_i)}
                    map_j = {val: pos for pos, val in enumerate(idx_j)}
                    pos_i = [map_i[s] for s in shared]
                    pos_j = [map_j[s] for s in shared]
                    aris.append(adjusted_rand_score(lbl_i[pos_i], lbl_j[pos_j]))
            return np.mean(aris) if aris else np.nan

        # Record Control (i)
        nc_stab = calc_stab(near_const_parts)
        nc_acc = np.mean(near_const_accs)
        records.append({
            "dataset": d,
            "model": "Control_NearConstant",
            "is_control": True,
            "stab": nc_stab,
            "acc": nc_acc,
            "mean_k": 2.0,
            "mean_min_frac": 1.0 / n_sub,
            "mean_max_frac": (n_sub - 1.0) / n_sub,
            "degen_rate": 1.0,
            "rule_i": (nc_stab >= 0.50) and (nc_acc <= 0.05),
            "rule_i_prime": False,
        })

        # Record Control (ii)
        rb_stab = calc_stab(rand_bal_parts)
        rb_acc = np.mean(rand_bal_accs)
        # class fracs
        u_y, c_y = np.unique(y, return_counts=True)
        records.append({
            "dataset": d,
            "model": "Control_RandomBalanced",
            "is_control": True,
            "stab": rb_stab,
            "acc": rb_acc,
            "mean_k": float(len(u_y)),
            "mean_min_frac": float(np.min(c_y) / n_total),
            "mean_max_frac": float(np.max(c_y) / n_total),
            "degen_rate": 0.0,
            "rule_i": (rb_stab >= 0.50) and (rb_acc <= 0.05),
            "rule_i_prime": False,
        })

        # -------------------------------------------------------------
        # 2. Real Evaluated Models (Item 2b)
        # -------------------------------------------------------------
        for m in MODELS:
            cluster_counts = []
            min_fracs = []
            max_fracs = []
            degen_flags = []
            partitions = []
            accuracies = []

            for sub_id in range(30):
                pfile = PARTITIONS_DIR / f"{d}_{m}_real_{sub_id}.npy"
                if not pfile.exists():
                    continue
                data = np.load(pfile, allow_pickle=True).item()
                sub_idx = data["sub_idx"]
                lbl = data["labels"]
                partitions.append((sub_idx, lbl))

                acc = adjusted_rand_score(y[sub_idx], lbl)
                accuracies.append(acc)

                u, counts = np.unique(lbl, return_counts=True)
                n_sub = len(lbl)
                cluster_counts.append(len(u))
                if len(u) < k_target:
                    min_frac = 0.0
                    max_frac = 1.0 if len(u) == 1 else np.max(counts) / n_sub
                    is_deg = True
                else:
                    min_frac = np.min(counts) / n_sub
                    max_frac = np.max(counts) / n_sub
                    is_deg = min_frac < 0.05
                min_fracs.append(min_frac)
                max_fracs.append(max_frac)
                degen_flags.append(is_deg)

            stab = calc_stab(partitions)
            mean_acc = np.mean(accuracies) if accuracies else np.nan
            mean_k = np.mean(cluster_counts)
            mean_min_f = np.mean(min_fracs)
            mean_max_f = np.mean(max_fracs)
            degen_rate = np.mean(degen_flags)

            rule_i = (stab >= 0.50) and (mean_acc <= 0.05)
            # Rule i': smallest cluster >= 5% in >= 90% of subsamples (degen_rate <= 0.10)
            rule_i_prime = rule_i and (degen_rate <= 0.10)

            records.append({
                "dataset": d,
                "model": m,
                "is_control": False,
                "stab": stab,
                "acc": mean_acc,
                "mean_k": mean_k,
                "mean_min_frac": mean_min_f,
                "mean_max_frac": mean_max_f,
                "degen_rate": degen_rate,
                "rule_i": rule_i,
                "rule_i_prime": rule_i_prime,
            })

    df = pd.DataFrame(records)
    out_csv = ROOT / "results" / "stability_degeneracy_audit.csv"
    df.to_csv(out_csv, index=False)
    print(f"[+] Saved degeneracy audit to {out_csv}")

    # Summary analysis
    models_only = df[~df["is_control"]]
    print("\n" + "=" * 80)
    print("RULE (i) vs AMENDED RULE (i') COMPARISON BY MODEL:")
    print("=" * 80)
    summary = models_only.groupby("model").agg(
        cohorts_rule_i=("rule_i", "sum"),
        cohorts_rule_i_prime=("rule_i_prime", "sum"),
    ).reset_index()
    print(summary.to_string(index=False))

    print("\n" + "=" * 80)
    print("PROSTATE DATASET DEGENERACY BREAKDOWN:")
    print("=" * 80)
    prostate_sub = df[df["dataset"] == "prostate"][
        ["model", "stab", "acc", "mean_k", "mean_min_frac", "mean_max_frac", "degen_rate", "rule_i", "rule_i_prime"]
    ]
    print(prostate_sub.to_string(index=False))

    print("\n" + "=" * 80)
    print("ALL PAIRS MEETING AMENDED RULE (i') (NON-DEGENERATE DISCORDANCE):")
    print("=" * 80)
    meets = models_only[models_only["rule_i_prime"]][
        ["dataset", "model", "stab", "acc", "mean_min_frac", "degen_rate"]
    ]
    print(meets.to_string(index=False))

    print("\n" + "=" * 80)
    print("REFERENCE CONTROLS:")
    print("=" * 80)
    ctrls = df[df["is_control"]][
        ["dataset", "model", "stab", "acc", "mean_min_frac", "degen_rate", "rule_i", "rule_i_prime"]
    ]
    print(ctrls.to_string(index=False))

    # Paired Bootstrap of Stability-Accuracy Gap (B=10000)
    # Resample cohorts with replacement
    rng = np.random.default_rng(42)
    cohorts = np.array(DATASETS)

    def bootstrap_gap(filtered_df):
        boot_gaps = []
        for _ in range(10000):
            b_cohorts = rng.choice(cohorts, size=len(cohorts), replace=True)
            sub = filtered_df[filtered_df["dataset"].isin(b_cohorts)]
            # cohort-level mean gap
            c_gaps = []
            for c in b_cohorts:
                c_df = filtered_df[filtered_df["dataset"] == c]
                if not c_df.empty:
                    c_gaps.append((c_df["stab"] - c_df["acc"]).mean())
            if c_gaps:
                boot_gaps.append(np.mean(c_gaps))
        obs_gap = (filtered_df["stab"] - filtered_df["acc"]).mean()
        low, high = np.percentile(boot_gaps, [2.5, 97.5])
        return obs_gap, low, high

    # (A) All pairs (unconstrained Rule i)
    gap_all, low_all, high_all = bootstrap_gap(models_only)
    print(f"\nPaired Bootstrap Gap (ALL pairs, including degenerate): {gap_all:+.3f} (95% CI: [{low_all:+.3f}, {high_all:+.3f}])")

    # (B) Excluding degenerate pairs (degen_rate <= 0.10)
    non_degen = models_only[models_only["degen_rate"] <= 0.10]
    gap_nd, low_nd, high_nd = bootstrap_gap(non_degen)
    print(f"Paired Bootstrap Gap (EXCLUDING degenerate pairs): {gap_nd:+.3f} (95% CI: [{low_nd:+.3f}, {high_nd:+.3f}])")


if __name__ == "__main__":
    main()
