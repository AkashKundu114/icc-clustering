#!/usr/bin/env python3
"""
generate_provenance_reconciliation.py
-------------------------------------
Generates audit/loop5_4/provenance_reconciliation.csv
Forensically documents all input artifacts used in Loop 5.3 and Loop 5.4,
including file size, SHA-256, Git blob SHA-1, Git tracking status, and consuming scripts.
"""

import os
import csv
import hashlib
import subprocess

artifacts = [
    {
        'path': 'results/evidence_recovery/recovered/results.json',
        'consuming_scripts': 'generate_task2.py (5.3), inspect_scaling.py (5.3), generate_friedman_validation.py (5.4)',
        'description': 'Master JSON results archive containing 1,430 exp3_1 fits and scaling runs'
    },
    {
        'path': 'results/evidence_recovery/recovered/stats.json',
        'consuming_scripts': 'execute_recomputations.py (5.2), generate_friedman_validation.py (5.4)',
        'description': 'Precomputed summary statistics JSON (N13, N12, HighD_N6)'
    },
    {
        'path': 'results/evidence_recovery/recovered/subsample_stability_summary.csv',
        'consuming_scripts': 'execute_recomputations.py (5.2), clustered_bootstrap.py (5.3), clustered_bootstrap_independent_verification.py (5.4)',
        'description': '72-cell subsample stability and accuracy matrix across 6 cohorts x 12 models'
    },
    {
        'path': 'results/evidence_recovery/recovered/exp2_real_high_d_factorial.csv',
        'consuming_scripts': 'execute_recomputations.py (5.2), generate_task2.py (5.3)',
        'description': '420-run factorial ablation experiment across 6 biomedical cohorts'
    },
    {
        'path': 'results/evidence_recovery/recovered/adversarial_autok_raw_results.csv',
        'consuming_scripts': 'execute_recomputations.py (5.2)',
        'description': '510-trial adversarial AutoK collapse dataset'
    },
    {
        'path': 'results/loop2/raw/exp5_baseline_comparison.csv',
        'consuming_scripts': 'generate_task2.py (5.3), generate_leukemia_reconciliation.py (5.4)',
        'description': 'Raw 5-seed baseline comparison results across datasets'
    },
    {
        'path': 'results/loop2/raw/exp5_baseline_comparison.json',
        'consuming_scripts': 'execute_recomputations.py (5.2)',
        'description': 'Precomputed 5-seed baseline comparison summary JSON'
    },
    {
        'path': 'results/loop2/raw/exp6_scalability.csv',
        'consuming_scripts': 'check_exp6.py (5.3), scalability_forensic_report.md (5.3, 5.4)',
        'description': 'Raw scalability profiling logs (N=100 to N=50,000)'
    },
    {
        'path': 'results/loop2/raw/exp4_anchor_budget.csv',
        'consuming_scripts': 'leukemia_ci_reconciliation.md (5.3, 5.4)',
        'description': 'Anchor budget sweep raw observations (source of spurious 0.3800/0.7960 values)'
    },
    {
        'path': 'results/loop2/raw/exp3_inductive_geometry.csv',
        'consuming_scripts': 'leukemia_ci_reconciliation.md (5.3, 5.4)',
        'description': 'Inductive geometry sweep raw observations'
    },
    {
        'path': 'paper/tables/table02_real_data_stability.tex',
        'consuming_scripts': 'Task 1, 2, 8 audits',
        'description': 'Manuscript Table 2 LaTeX source (subsample stability and accuracy)'
    },
    {
        'path': 'paper/tables/table04_sample_scaling.tex',
        'consuming_scripts': 'Task 4 scalability audit',
        'description': 'Manuscript Table 4 LaTeX source (traced RAM vs sample size N)'
    },
    {
        'path': 'paper/tables/table06_omnibus_benchmark_ari.tex',
        'consuming_scripts': 'Task 5 Friedman validation, Task 8 claim audit',
        'description': 'Manuscript Table 6 LaTeX source (13 benchmarks x 12 models)'
    }
]

out_records = []
for a in artifacts:
    rel_path = a['path']
    exists = os.path.exists(rel_path)
    file_size = os.path.getsize(rel_path) if exists else -1
    
    if exists:
        raw_bytes = open(rel_path, 'rb').read()
        sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
        try:
            git_blob = subprocess.check_output(['git', 'hash-object', rel_path]).decode().strip()
        except:
            git_blob = 'N/A'
    else:
        sha256_hash = 'MISSING'
        git_blob = 'MISSING'

    # Check Git status
    try:
        status_out = subprocess.check_output(['git', 'status', '--porcelain', rel_path]).decode().strip()
        check_ignore = subprocess.run(['git', 'check-ignore', rel_path], capture_output=True).returncode == 0
        tracked_out = subprocess.run(['git', 'ls-files', '--error-unmatch', rel_path], capture_output=True).returncode == 0
    except:
        status_out = 'ERROR'
        check_ignore = False
        tracked_out = False

    git_status = 'TRACKED_COMMITTED' if tracked_out and not status_out else ('IGNORED' if check_ignore else ('UNTRACKED' if not tracked_out else 'MODIFIED'))

    out_records.append({
        'Relative_Path': rel_path,
        'File_Exists': exists,
        'File_Size_Bytes': file_size,
        'SHA256_Hash': sha256_hash,
        'Git_Blob_SHA1': git_blob,
        'Git_Tracking_Status': git_status,
        'Is_Git_Ignored': check_ignore,
        'Consuming_Audit_Scripts': a['consuming_scripts'],
        'Artifact_Description': a['description']
    })

out_csv = 'audit/loop5_4/provenance_reconciliation.csv'
fieldnames = [
    'Relative_Path', 'File_Exists', 'File_Size_Bytes', 'SHA256_Hash',
    'Git_Blob_SHA1', 'Git_Tracking_Status', 'Is_Git_Ignored',
    'Consuming_Audit_Scripts', 'Artifact_Description'
]

with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in out_records:
        writer.writerow(r)

print(f"Successfully wrote {len(out_records)} provenance records to {out_csv}")
