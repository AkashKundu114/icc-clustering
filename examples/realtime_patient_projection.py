"""
Real-Time Patient Query Projection & Conformal Certainty Sets (Case Study 3)
============================================================================
Demonstrates the inductive deployment of ICC-v2 for point-of-care clinical
decision support. Traditional consensus clustering is strictly transductive and
requires re-clustering the entire historical patient database (O(N^2)) whenever
a new patient sample arrives.

ICC-v2 solves this through:
1. Closed-form stability-weighted centroid projection: O(N_test * K * |F_gate|)
   latency (< 1 ms per patient biopsy).
2. Split-conformal uncertainty calibration: Outputting prediction sets C(x) with
   finite-sample guaranteed coverage (1 - alpha >= 90%).
3. Ambiguity & Abstention handling: Flagging borderline cases (|C(x)| > 1) for
   senior pathological review and novel outliers (|C(x)| = 0) for exploratory sequencing.
"""

import time

import numpy as np
from scipy.optimize import linear_sum_assignment

from cicc import InductiveConsensusClusterer
from icc.datasets.registry import load_dataset


def run_realtime_patient_projection():
    print("=" * 78)
    print("CLINICAL CASE STUDY: REAL-TIME POINT-OF-CARE INDUCTIVE DECISION SUPPORT")
    print("=" * 78)

    # 1. Load patient microarray cohort
    X, y, meta = load_dataset("leukemia")
    N, D = X.shape
    print("\n[1] Reference Cohort Initialization:")
    print(f"  Benchmark: {meta.get('display_name', 'Leukemia')} (N = {N} patients, D = {D} features)")

    # 2. Split into Historical Reference Cohort (80%) and Prospective New Patients (20%)
    rng = np.random.default_rng(42)
    indices = rng.permutation(N)
    n_train = int(0.80 * N)
    ref_idx, query_idx = indices[:n_train], indices[n_train:]

    X_ref, y_ref = X[ref_idx], y[ref_idx]
    X_query, y_query = X[query_idx], y[query_idx]
    n_query = len(query_idx)

    print(f"  Historical Reference Patients: N_ref   = {len(ref_idx)} (Model fitting & conformal calibration)")
    print(f"  Prospective Incoming Queries:  N_query = {n_query} (Point-of-care real-time evaluation)")

    # 3. Fit Inductive Consensus Clusterer with Conformal Calibration
    print("\n[2] Fitting Inductive Consensus Model on Historical Cohort...")
    t0 = time.perf_counter()
    clusterer = InductiveConsensusClusterer(
        n_clusters=2,
        n_anchors=30,
        n_base_models=20,
        subspace_rate=0.30,
        alpha=0.10,          # 90% finite-sample coverage guarantee
        random_state=42,
    )
    clusterer.fit(X_ref)
    fit_time = time.perf_counter() - t0
    print(f"  Reference Consensus & Conformal Calibration completed in {fit_time:.3f} s.")

    # Hungarian alignment to map unsupervised clusters to ground-truth labels for evaluation
    contingency = np.zeros((2, 2), dtype=int)
    for true_c, pred_c in zip(y_ref, clusterer.labels_):
        contingency[true_c, pred_c] += 1
    row_ind, col_ind = linear_sum_assignment(-contingency)
    cluster_to_class = {col: row for row, col in zip(row_ind, col_ind)}
    class_to_cluster = {v: k for k, v in cluster_to_class.items()}
    mapped_y_query = np.array([class_to_cluster[y_val] for y_val in y_query])

    # 4. Measure Inductive Projection Latency
    print("\n[3] Point-of-Care Real-Time Projection Benchmark:")
    t_start = time.perf_counter()
    conformal_result = clusterer.predict_conformal(X_query, y_new=mapped_y_query)
    total_proj_time_ms = (time.perf_counter() - t_start) * 1000
    latency_per_sample_us = (total_proj_time_ms / n_query) * 1000

    print(f"  Total Projection Time for {n_query} biopsies: {total_proj_time_ms:.3f} ms")
    print(f"  Per-Patient Projection Latency:         {latency_per_sample_us:.1f} microseconds (< 1 ms)")
    cov = conformal_result.empirical_coverage if conformal_result.empirical_coverage is not None else 0.0
    print(f"  Empirical Out-of-Sample Coverage:       {cov * 100:.1f}%")
    print(f"  Average Prediction Set Cardinality:     {conformal_result.average_set_size:.2f} clusters")

    # 5. Patient-by-Patient Diagnostic Report
    print("\n[4] Individual Prospective Patient Diagnostic Sets:")
    print("-" * 78)
    print(f"{'Patient ID':<12} {'Pathology':<12} {'Prediction Set C(x)':<22} {'P(ALL)':<10} {'P(AML)':<10} {'Status':<15}")
    print("-" * 78)

    subtype_names = {0: "ALL", 1: "AML"}
    for i in range(n_query):
        true_sub = subtype_names.get(int(y_query[i]), str(y_query[i]))
        c_set = conformal_result.prediction_sets[i]
        c_set_str = "{" + ", ".join(subtype_names[cluster_to_class[c]] for c in c_set) + "}"
        # Probability for ALL and AML
        p_all = conformal_result.probabilities[i, class_to_cluster[0]]
        p_aml = conformal_result.probabilities[i, class_to_cluster[1]]

        if conformal_result.is_singleton[i]:
            status = "High-Confidence"
        elif conformal_result.is_ambiguous[i]:
            status = "Flag: Ambiguous"
        else:
            status = "Flag: Outlier/Novel"

        print(f"Patient_{i+1:<4} {true_sub:<12} {c_set_str:<22} {p_all:<10.3f} {p_aml:<10.3f} {status:<15}")

    print("-" * 78)
    print("Clinical Interpretation:")
    print("  - High-Confidence singletons allow immediate targeted therapy.")
    print("  - Ambiguous biopsies trigger manual review or secondary immunohistochemistry,")
    print("    preventing toxic misclassification in borderline clinical presentations.")
    print("=" * 78)


if __name__ == "__main__":
    run_realtime_patient_projection()
