# Audit Controls & Extended Reproducibility Suite

This directory contains the experimental verification scripts and empirical result data generated during the independent research audit and extended benchmark study.

---

## 1. Directory Structure

* **`src/`**: Executable verification and benchmark scripts
  * `a2_controls.py`: Multi-seed synthetic and real controls comparing legacy vs. robust vs. Gaussian-null pool selection.
  * `a2_filter_controls.py`: Verification that single-pass filtering alone (K-Means on screened features) fails without subspace consensus.
  * `a2_random_control.py`: Baseline control verifying that consensus on unguided random pools collapses to near-chance.
  * `a3_embedding.py`: Principal angle cosine verification proving exact eigenspace span ($1.000$) between bipartite Laplacian and full co-association.
  * `a3_paths.py`: Numerical verification of dense ($N \le 2000$) vs. scalable subsampled ($N > 2000$) paths.
  * `e3_pool_curve.py`: 7-point pool-size sensitivity curve (2% to 100%) comparing BC-ranked vs. random pools.
  * `e3_label_free_selector.py`: Unsupervised pool-size selection evaluation demonstrating the distance concentration trap.
  * `e3b_label_free_selector.py`: External reviewer's label-free pool-size selection protocol (silhouette & stability criteria).
  * `e5_exp1_rerun.py`: Re-run of Exp1 pseudo-label generalization test across 4 noise regimes $\times$ 4 downstream classifiers.
  * `e5_missing_rerun.py`: Re-run of missing-data evaluation across all 8 cached datasets and 5 missing rates.
  * `e1_extended_benchmarks.py`: Extended multi-domain evaluation spanning 21 real-world datasets across 10 clustering models.

* **`data/`**: Raw CSV trial results and summary tables
  * `a2_syn.csv`, `a2_real.csv`: Core control benchmark data.
  * `a2_filter_controls.csv`: Numerical proof that filtering alone is insufficient.
  * `a2_random_control.csv`: Empirical verification of random pool failure.
  * `e3_pool_curve.csv`: 8-dataset pool-size sensitivity curve.
  * `e3_label_free_selector_eval.csv`: Unsupervised metric evaluation across all pool sizes.
  * `e3_label_free_selector_summary.csv`: Summary comparing Oracle best fraction vs. legacy 15% floor vs. internal criteria.
  * `e3b_selector.csv`: Reviewer E3b selection trial records across 8 datasets $\times$ 5 seeds.
  * `e5_exp1_pseudolabel_rerun.csv`: E5 pseudo-label sweep trial evaluations ($320$ rows).
  * `e5_missing_rerun.csv`: E5 missing-data evaluation across 8 datasets $\times$ 5 rates $\times$ 5 seeds ($200$ rows).
  * `e1_extended_benchmarks.csv`: Complete trial-level records across 21 datasets $\times$ 10 models $\times$ 5 seeds ($1,050$ rows).
  * `e1_extended_summary.csv`: Grand mean ARI matrix across all 21 benchmarks.

---

## 2. Reproduction Instructions

To execute any verification script, run from repository root:

```powershell
# Run the 21-dataset extended benchmark:
python experiments/audit_controls/src/e1_extended_benchmarks.py

# Run the pool-size sensitivity sweep:
python experiments/audit_controls/src/e3_pool_curve.py

# Run the unsupervised selector evaluation:
python experiments/audit_controls/src/e3_label_free_selector.py
```
