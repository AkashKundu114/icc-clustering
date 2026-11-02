# Proposed rights-aware release layout

```text
release/
├── README.md
├── LICENSE
├── environment.lock
├── configs/
├── scripts/
│   ├── verify_aggregate.py
│   ├── verify_partitions.py       # include only if Tier 2 inputs are cleared
│   └── rerun_experiment.py        # only after producer/configuration recovery
├── data_acquisition/
│   ├── six_cohort_sources.csv
│   └── thirteen_benchmark_sources.csv
├── results/
│   ├── aggregate/                 # source/provenance documented
│   ├── partitions/                # only if redistribution allowed
│   └── benchmark_scores/          # raw saved scores; execution status explicit
├── manifests/
│   ├── inputs.csv
│   ├── outputs.csv
│   ├── sample_ids.csv             # only if permitted and de-identified
│   └── SHA256SUMS
└── manuscript/
    ├── main.tex
    ├── references.bib
    ├── tables/
    └── figures/
```

Current public repository satisfies only the aggregate subpackage. No partition or input dataset is cleared for bundling by this audit. Yale B image files must be excluded absent written permission. Raw and transformed caches, sample IDs and partitions require source-specific rights and privacy review; a derived representation is not automatically rights-free. The exact intended manuscript must be frozen and hashed before it is included.
