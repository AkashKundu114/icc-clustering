# ICC clustering documentation

This guide describes the research software, its configured data loaders and benchmarks, and the limits of the available evidence. It is written for researchers who have not used this repository before.

## Start here

- [Research overview](research-overview.md): question, scope, and interpretation.
- [Methodology](methodology.md): the distinct stability and external-ARI designs.
- [Datasets](datasets.md): sources, configured shapes, and access restrictions.
- [Results](results.md): verified descriptive findings and their limits.
- [Statistical analysis](statistical-analysis.md): estimands, dependence, and sensitivity.
- [Limitations](limitations.md): evidence and implementation caveats.
- [Reproducibility](reproducibility.md): tested commands and three evidence tiers.
- [Software architecture](software-architecture.md): code layout and entry points.
- [FAQ](faq.md): common practical questions.

The code API is under `src/`; package metadata and dependencies are in `pyproject.toml`; dataset registry configuration is in `configs/datasets.yaml`; command-line helpers are under `scripts/`; tests are under `tests/`. The public repository currently does not provide the saved partitions or raw benchmark score files needed to reproduce the primary empirical results from the underlying observations.
