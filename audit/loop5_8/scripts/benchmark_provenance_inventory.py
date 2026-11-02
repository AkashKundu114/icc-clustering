"""Rebuild benchmark seed schedule and input artifact inventory from local FYP inputs.

Expected inputs: D:/Final Year Project/results/passF/benchmark_matrix_passF.csv,
results/exp3_cohirf_benchmark.csv, results/passF/benchmark_matrix_summary_passF.csv,
scripts/run_phase3_experiments.py, experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py,
configs/datasets.yaml, and Loop 5.7 benchmark/provenance reports.
Outputs: audit/loop5_8/benchmark_seed_schedule.csv and artifact_manifest.csv.
No model fits are executed.
"""
from pathlib import Path
import hashlib, subprocess
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]
FYP=Path(r"D:\Final Year Project")
OUT=ROOT/"audit"/"loop5_8"
def main():
    a=pd.read_csv(FYP/"results/passF/benchmark_matrix_passF.csv")
    b=pd.read_csv(FYP/"results/exp3_cohirf_benchmark.csv")
    rows=[]
    for (ds,method),g in a.groupby(["dataset","model"],sort=True):
        seeds=sorted(map(int,g.seed.unique()))
        rows.append(dict(dataset=ds,method=method,source_file="results/passF/benchmark_matrix_passF.csv",n_rows=len(g),n_unique_seeds=len(seeds),seed_min=min(seeds),seed_max=max(seeds),seed_values=";".join(map(str,seeds)),schedule_class="Pass F saved-row schedule"))
    for (ds,method),g in b.groupby(["dataset","model"],sort=True):
        seeds=sorted(map(int,g.seed.unique()))
        rows.append(dict(dataset=ds,method=method,source_file="results/exp3_cohirf_benchmark.csv",n_rows=len(g),n_unique_seeds=len(seeds),seed_min=min(seeds),seed_max=max(seeds),seed_values=";".join(map(str,seeds)),schedule_class="CoHiRF saved-row schedule"))
    pd.DataFrame(rows).to_csv(OUT/"benchmark_seed_schedule.csv",index=False)
    items=[FYP/"results/passF/benchmark_matrix_passF.csv",FYP/"results/exp3_cohirf_benchmark.csv",FYP/"results/passF/benchmark_matrix_summary_passF.csv",FYP/"scripts/run_phase3_experiments.py",FYP/"experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py",FYP/"configs/datasets.yaml",ROOT/"audit/loop5_7/benchmark_scope_verification.md",ROOT/"audit/loop5_7/provenance_chain.md"]
    out=[]
    for p in items:
        raw=p.read_bytes(); under=p.is_relative_to(FYP); repo=FYP if under else ROOT
        tracked=subprocess.run(["git","-C",str(repo),"ls-files","--error-unmatch",p.relative_to(repo).as_posix()],capture_output=True).returncode==0
        out.append(dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),classification="raw saved scores" if p.suffix==".csv" and "summary" not in p.name else ("source/configuration" if p.suffix in (".py",".yaml") else "prior audit supporting document"),tracked_in_target_repo=tracked if not under else False,tracked_in_fyp_head=tracked if under else False,modified_time_utc=pd.Timestamp(p.stat().st_mtime,unit="s",tz="UTC").isoformat()))
    pd.DataFrame(out).to_csv(OUT/"artifact_manifest.csv",index=False)
if __name__=="__main__": main()
