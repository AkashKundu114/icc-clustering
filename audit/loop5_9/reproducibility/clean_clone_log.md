# Clean clone reproduction log

- Remote: `https://github.com/AkashKundu114/icc-clustering.git`
- Clone: `D:\temp\icc_loop59_clean_20261102` (fresh, shallow; not a reuse of the local ignored files).
- Exact `HEAD`: `d0c4665af327ec284d931c94f9658309ec13763c`, matching fetched `origin/main` at the Loop 5.9 baseline.
- Command: `git clone --quiet --depth 1 https://github.com/AkashKundu114/icc-clustering.git D:\temp\icc_loop59_clean_20261102`; exit code 0.
- Environment: Windows PowerShell; Python 3.14.6. Aggregate script uses standard library only; no dependency installation was needed.
- Tier 1 command: `python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py`; exit code 0.
- Script SHA-256: `3cac0aff64d4d949622cfc163e3f15cbf654759a890c908bba193c55fbeb0a04`.
- Input SHA-256: `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f`.
- Captured stdout: `audit/loop5_9/tier1_fresh_clone_output.json`, SHA-256 `538f5e9ce1026689eeebf5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`.
- Output: 72 rows; 6 datasets; 12 methods; mean stability 0.5165860620823638; mean external ARI 0.0523121821722892; mean gap 0.46427387991007457; median gap 0.44840681694162077.
- Runtime duration was not captured; no duration is claimed.

An additional isolated-environment check used a newly created empty virtual environment at `D:\temp\loop59_tier1_venv` (Python 3.14.6; no packages installed). From the same clean clone, the same Tier 1 command exited 0 and emitted byte-identical stdout (SHA-256 `538f5e9ce1026689eeebf5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`). This confirms Tier 1 needs only the standard library; it does not change the Tier 2 or Tier 3 limitations.

The clone has no `results/stability/partitions/`, `results/stability/runs/`, `data/cache/*.npz`, raw Pass F or CoHiRF score CSVs, nor manuscript package. Tier 2 inputs are absent; Tier 3 was not run. The aggregate script writes `audit/loop5_6/minimum_aggregate_package/recomputed.json`; after execution, `git status --short` shows that one expected untracked generated output in the temporary clone. The source clone was clean before the command, no tracked source changed, and nothing was pushed to GitHub. The lead independently repeated the same clone and command at the exact baseline commit; its captured stdout hash is listed in `tier1_fresh_clone_output.json`.
