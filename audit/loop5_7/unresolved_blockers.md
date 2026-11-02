# Unresolved blockers before submission

- **Run-to-input provenance:** per-fit records lack cache SHA, input path, sample IDs, preprocessing fingerprint and source commit. Tracked cache copies match byte-for-byte but are not referenced in each run.
- **Original execution identity:** `49f3882...` is a code/protocol/summary commit, not verified execution evidence. No original experiment-execution commit can be assigned.
- **Public evidence:** raw stability partitions/runs and 13-dataset raw score CSVs are absent from current public main; FYP branch not remotely advertised. Zenodo record has no downloadable files and restricted access.
- **Audit package integrity:** stale aggregate-only `recomputed_summary.json`, stale evidence inventory, false original-execution/final-commit entries and order-sensitive scripts remain committed in Loop 5.6. Regenerate a coherent package in a new audit/release commit; do not overwrite history.
- **Bootstrap:** resolve cell-weighted point versus equal-cohort resampling estimand, reproduce exact interval, and frame six-cohort bootstrap as exploratory.
- **Seed schedule:** reconcile benchmark raw schedules (Pass F 0–29/0–9; CoHiRF 42–71/42–51) with manuscript lines 366/556 and retained code/config.
- **Duplicate partitions:** explain three exact cross-mode groups, including degenerate CNS CoHiRF real/null repeat 17, and assess whether intentional.
- **Manuscript version:** the reviewed `paper/manuscript/main.tex` is ignored/untracked; identify and commit the exact submission version after revisions.
- **Data rights:** verify upstream licenses/terms and attribution before redistributing any raw or transformed third-party dataset.
- **Other claims:** ablation, scaling, seed stability, PCA/Prostate mechanism, clinical implications and ICC superiority claims require separate auditable evidence; this Loop did not validate them.
